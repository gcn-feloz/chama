import cv2
from config import CAMERA_CONFIG

class StreamCapture:
    def __init__(self):
        """
        Inicializa a captura de vídeo da câmera
        """
        # Inicializa a captura usando o ID da câmera configurado
        self.capture = cv2.VideoCapture(CAMERA_CONFIG['device_id'])
        
        # Configura as propriedades da câmera
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_CONFIG['frame_width'])
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_CONFIG['frame_height'])
        self.capture.set(cv2.CAP_PROP_FPS, CAMERA_CONFIG['fps'])
        
        if not self.capture.isOpened():
            raise RuntimeError("Não foi possível inicializar a câmera")
    
    def get_frame(self):
        """
        Captura e retorna o próximo frame do vídeo
        Returns:
            np.ndarray: Frame capturado ou None se houver erro
        """
        if not self.capture.isOpened():
            return None
            
        ret, frame = self.capture.read()
        if not ret:
            return None
            
        # Redimensiona o frame para o tamanho configurado
        frame = cv2.resize(frame, 
                         (CAMERA_CONFIG['frame_width'], 
                          CAMERA_CONFIG['frame_height']))
            
        return frame
        
    def release(self):
        """
        Libera os recursos de captura de vídeo
        """
        if self.capture:
            self.capture.release()