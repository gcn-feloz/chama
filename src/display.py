"""
Módulo de interface gráfica.
Gerencia a exibição dos frames e informações na tela.
"""
import cv2
import numpy as np
from config import DISPLAY_CONFIG

class Display:
    def __init__(self):
        """Inicializa o display com as configurações especificadas"""
        self.window_name = DISPLAY_CONFIG['window_name']
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = DISPLAY_CONFIG['font_scale']
        self.line_thickness = DISPLAY_CONFIG['line_thickness']
        self.colors = DISPLAY_CONFIG['colors']
        
        # Cria a janela principal
        cv2.namedWindow(self.window_name)
        
    def show_frame(self, frame, detections=None, alerts=None, fps=None):
        """
        Exibe o frame com as detecções e alertas
        
        Args:
            frame (numpy.ndarray): Frame a ser exibido
            detections (list): Lista de detecções para mostrar
            alerts (list): Lista de alertas ativos
            fps (float): FPS atual para exibir
        """
        if frame is None:
            return
            
        # Cria uma cópia do frame para desenhar
        display_frame = frame.copy()
        
        # Desenha as detecções
        if detections:
            self._draw_detections(display_frame, detections)
            
        # Desenha os alertas
        if alerts:
            self._draw_alerts(display_frame, alerts)
            
        # Mostra FPS se necessário
        if DISPLAY_CONFIG['show_fps'] and fps is not None:
            self._draw_fps(display_frame, fps)
            
        # Exibe o frame
        cv2.imshow(self.window_name, display_frame)
        
    def _draw_detections(self, frame, detections):
        """Desenha as caixas de detecção e pontos-chave"""
        for det in detections:
            # Desenha bounding box
            x1, y1, x2, y2 = det['bbox']
            cv2.rectangle(frame, (x1, y1), (x2, y2), 
                         self.colors['detection'], self.line_thickness)
            
            # Mostra confiança
            conf_text = f"{det['confidence']:.2f}"
            cv2.putText(frame, conf_text, (x1, y1-10), self.font,
                       self.font_scale, self.colors['text'], self.line_thickness)

    def _draw_alerts(self, frame, alerts):
        """Desenha as informações dos alertas ativos"""
        for i, alert in enumerate(alerts):
            text = f"Mesa {alert['table']}"
            pos = (10, 30 + i * 30)
            cv2.putText(frame, text, pos, self.font,
                       self.font_scale, self.colors['alert'], self.line_thickness)

    def _draw_fps(self, frame, fps):
        """Desenha o FPS atual"""
        text = f"FPS: {fps:.1f}"
        cv2.putText(frame, text, (10, frame.shape[0] - 10), self.font,
                    self.font_scale, self.colors['text'], self.line_thickness)
    def destroy(self):
        """Fecha todas as janelas"""
        cv2.destroyAllWindows()
