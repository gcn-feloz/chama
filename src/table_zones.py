import numpy as np
import cv2
import json

class TableZoneManager:
    """
    Gerencia as zonas das mesas e verifica interseções com detecções
    """
    def __init__(self, zones_file='table_zones.json'):
        """
        Inicializa o gerenciador de zonas
        Args:
            zones_file: Arquivo JSON com a configuração das zonas
        """
        self.zones = []
        self.load_zones(zones_file)
    
    def load_zones(self, zones_file):
        """
        Carrega as zonas das mesas do arquivo JSON
        Args:
            zones_file: Caminho para o arquivo de configuração
        """
        try:
            with open(zones_file, 'r') as f:
                data = json.load(f)
                for table in data['tables']:
                    self.zones.append({
                        'id': table['id'],
                        'name': table['name'],
                        'points': np.array(table['points'], dtype=np.int32)
                    })
        except FileNotFoundError:
            print(f"Arquivo de zonas {zones_file} não encontrado")
    
    def check_detection(self, detection):
        """
        Verifica se uma detecção está dentro de alguma zona de mesa
        Args:
            detection: Dicionário com bbox da detecção
        Returns:
            dict or None: Informações da mesa se houver interseção
        """
        x1, y1, x2, y2 = detection['bbox']
        center_point = (int((x1 + x2) / 2), int((y1 + y2) / 2))
        
        for zone in self.zones:
            # Verifica se o ponto central da pessoa está dentro do polígono da mesa
            if cv2.pointPolygonTest(zone['points'], center_point, False) >= 0:
                return zone
        
        return None
    
    def draw_zones(self, frame):
        """
        Desenha as zonas das mesas no frame
        Args:
            frame: Frame do vídeo
        Returns:
            np.ndarray: Frame com as zonas desenhadas
        """
        display_frame = frame.copy()
        
        for zone in self.zones:
            # Desenha o polígono da mesa
            cv2.polylines(display_frame, 
                         [zone['points']], 
                         True, 
                         (0, 255, 0), 
                         2)
            
            # Adiciona o nome da mesa
            center = zone['points'].mean(axis=0).astype(int)
            cv2.putText(display_frame,
                       zone['name'],
                       tuple(center),
                       cv2.FONT_HERSHEY_SIMPLEX,
                       0.5,
                       (0, 255, 0),
                       2)
                       
        return display_frame
        
    def save_zones(self, filename='table_zones.json'):
        """
        Salva as configurações das zonas em um arquivo JSON
        Args:
            filename: Nome do arquivo para salvar
        """
        config = {
            "tables": [
                {
                    "id": zone['id'],
                    "name": zone['name'],
                    "points": zone['points'].tolist()
                }
                for zone in self.zones
            ]
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(config, f, indent=4)
            print(f"\nConfigurações salvas em {filename}")
            print(f"{len(self.zones)} mesas configuradas")
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
            
    def clear_zones(self):
        """
        Limpa todas as zonas configuradas
        """
        self.zones = []