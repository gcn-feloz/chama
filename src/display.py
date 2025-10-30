import cv2
import numpy as np
from config import DISPLAY_CONFIGS

class DisplayManager:
    def __init__(self):
        """
        Inicializa o gerenciador de exibição com as configurações do config.py
        """
        self.window_name = DISPLAY_CONFIGS['window_name']
        self.font_scale = DISPLAY_CONFIGS['font_scale']
        self.thickness = DISPLAY_CONFIGS['thickness']
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        
    def show_frame(self, frame, detections, alerts=None):
        """
        Mostra o frame com as detecções e alertas
        Args:
            frame (np.ndarray): Frame do vídeo
            detections (list): Lista de detecções
            alerts (list): Lista de alertas ativos
        """
        if frame is None:
            return
            
        # Cria uma cópia do frame para não modificar o original
        display_frame = frame.copy()
        
        # Desenha as detecções
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            conf = detection['confidence']
            
            # Desenha o retângulo da detecção
            cv2.rectangle(display_frame, 
                        (x1, y1), (x2, y2),
                        (0, 255, 0),
                        self.thickness)
            
            # Adiciona o texto de confiança
            text = f"Conf: {conf:.2f}"
            cv2.putText(display_frame,
                       text,
                       (x1, y1 - 10),
                       self.font,
                       self.font_scale,
                       (0, 255, 0),
                       self.thickness)
        
        # Desenha os alertas, se houver
        if alerts:
            for i, alert in enumerate(alerts):
                text = f"Alert: {alert['table']} - {alert['status']}"
                cv2.putText(display_frame,
                           text,
                           (10, 30 + i * 30),
                           self.font,
                           self.font_scale,
                           (0, 0, 255),
                           self.thickness)
        
        # Mostra o frame
        cv2.imshow(self.window_name, display_frame)
        cv2.waitKey(1)
        
    def close(self):
        """
        Fecha todas as janelas
        """
        cv2.destroyAllWindows()
