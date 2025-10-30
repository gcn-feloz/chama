"""
Módulo de captura de vídeo.
Gerencia a captura de frames da câmera.
"""
import cv2
from config import CAMERA_CONFIG

class Camera:
    def __init__(self):
        """Inicializa a câmera com as configurações especificadas"""
        self.cap = cv2.VideoCapture(CAMERA_CONFIG['device_id'])
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_CONFIG['frame_width'])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_CONFIG['frame_height'])
        self.cap.set(cv2.CAP_PROP_FPS, CAMERA_CONFIG['fps'])
        
        if not self.cap.isOpened():
            raise RuntimeError("Não foi possível inicializar a câmera")

    def read(self):
        """
        Captura um frame da câmera
        Returns:
            numpy.ndarray: Frame capturado ou None se houver erro
        """
        success, frame = self.cap.read()
        if not success:
            return None
        return frame

    def release(self):
        """Libera os recursos da câmera"""
        if self.cap:
            self.cap.release()