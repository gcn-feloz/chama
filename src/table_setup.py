import cv2
import json
import numpy as np
from stream_capture import StreamCapture

WINDOW_NAME = "Configuracao de Mesas"

class TableSetup:
    def __init__(self):
        self.zones = []          # Lista de zonas já definidas
        self.current_points = [] # Pontos da mesa atual
        self.stream = StreamCapture()
        
    def _draw_interface(self, frame):
        """
        Desenha a interface de configuração
        
        Args:
            frame: Frame a ser desenhado
            
        Returns:
            Frame com a interface desenhada
        """
        display_frame = frame.copy()
        return display_frame
        
        # Desenha as zonas já definidas
        for i, zone in enumerate(self.zones):
            # Desenha o polígono da mesa
            pts = zone.reshape((-1, 1, 2))
            cv2.polylines(display_frame, [pts], True, (0, 255, 0), 2)
            
            # Adiciona o número da mesa
            center = np.mean(zone, axis=0, dtype=np.int32)
            cv2.putText(display_frame, f"Mesa {i+1}", 
                       tuple(center), 
                       cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (0, 255, 0), 2)
        
        # Desenha os pontos da mesa atual
        for i, point in enumerate(self.current_points):
            # Desenha o ponto
            cv2.circle(display_frame, point, 5, (0, 0, 255), -1)
            # Mostra o número do ponto
            cv2.putText(display_frame, str(i+1), 
                       (point[0]+10, point[1]+10),
                       cv2.FONT_HERSHEY_SIMPLEX,
                       0.5, (0, 0, 255), 2)
            
            # Conecta os pontos com linhas
            if i > 0:
                cv2.line(display_frame, 
                        self.current_points[i-1],
                        point,
                        (255, 0, 0), 2)
                        
            # Fecha o polígono se tiver todos os pontos
            if i == 3:
                cv2.line(display_frame,
                        self.current_points[3],
                        self.current_points[0],
                        (255, 0, 0), 2)
        
        # Adiciona instruções na tela
        instructions = [
            f"Mesa atual: {len(self.zones) + 1}",
            f"Pontos: {len(self.current_points)}/4",
            "R: Recomeçar mesa",
            "S: Salvar e sair",
            "Q: Sair sem salvar"
        ]
        
        for i, text in enumerate(instructions):
            cv2.putText(display_frame, text,
                       (10, 30 + i * 30),
                       cv2.FONT_HERSHEY_SIMPLEX,
                       0.6, (255, 255, 255), 2)
        
    def setup_tables(self):
        """
        Interface principal para configuração das mesas
        """
        print("\n=== Configuração das Mesas ===")
        print("1. Clique em 4 pontos para definir cada mesa")
        print("2. Os pontos devem ser marcados em sentido horário")
        print("3. Controles:")
        print("   R - Recomeçar mesa atual")
        print("   S - Salvar configuração")
        print("   Q - Sair sem salvar\n")
        
        # Captura primeiro frame
        frame = self.stream.get_frame()
        if frame is None:
            print("Erro ao capturar frame inicial")
            return
            
        # Primeiro mostra a janela com o frame inicial
        cv2.imshow(WINDOW_NAME, frame)
        cv2.waitKey(1)  # Necessário para criar a janela
        
        # Depois configura o callback do mouse
        cv2.namedWindow(WINDOW_NAME)
        cv2.setMouseCallback(WINDOW_NAME, self._mouse_callback)
        
        while True:
            # Atualiza o frame
            frame = self.stream.get_frame()
            if frame is not None:
                self.frame = frame
            
            # Desenha a interface
            # Desenha interface e mostra o frame
            display_frame = self._draw_interface(self.frame)
            cv2.imshow(WINDOW_NAME, display_frame)
            
            # Processa comandos do teclado
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                self._save_zones()
                break
            elif key == ord('r'):
                self.current_points = []
            elif key == ord('z') and len(self.zones) > 0:
                self.zones.pop()  # Remove última mesa
                
        # Limpa recursos
        cv2.destroyAllWindows()
        self.stream.release()
        
        cv2.destroyAllWindows()
        self.stream.release()
        
    def _mouse_callback(self, event, x, y, flags, param):
        """
        Callback para eventos do mouse durante a configuração das mesas
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            # Adiciona novo ponto apenas se não tivermos 4 pontos ainda
            if len(self.current_points) < 4:
                self.current_points.append((x, y))
                print(f"Ponto {len(self.current_points)} adicionado: ({x}, {y})")
                
                # Se completou 4 pontos, cria uma nova zona
                if len(self.current_points) == 4:
                    self.zones.append(np.array(self.current_points, dtype=np.int32))
                    print(f"Mesa {len(self.zones)} definida!")
                    self.current_points = []  # Limpa para próxima mesa
                
    def _save_zones(self):
        """
        Salva as zonas das mesas em um arquivo JSON
        """
        if not self.zones:
            print("Nenhuma mesa definida para salvar!")
            return
            
        config = {
            "tables": [
                {
                    "id": i + 1,
                    "name": f"Mesa {i + 1}",
                    "points": zone.tolist()  # Converte array numpy para lista
                }
                for i, zone in enumerate(self.zones)
            ]
        }
        
        try:
            with open('table_zones.json', 'w') as f:
                json.dump(config, f, indent=4)
            print(f"\nConfigurações salvas! {len(self.zones)} mesas definidas.")
            for i, zone in enumerate(self.zones):
                print(f"Mesa {i+1}: {len(zone)} pontos")
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
        
        with open('table_zones.json', 'w') as f:
            json.dump(config, f, indent=4)
            
        print("Configuração das mesas salva com sucesso!")