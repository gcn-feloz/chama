"""
Módulo de detecção de gestos.
Utiliza YOLOv8 para detecção de pose e análise de gestos.
"""
import cv2
import numpy as np
from ultralytics import YOLO
from config import MODEL_CONFIG, GESTURE_CONFIG

class GestureDetector:
    def __init__(self):
        """Inicializa o detector de gestos usando YOLOv8"""
        try:
            # Carrega o modelo YOLOv8 para detecção de pose
            self.model = YOLO(MODEL_CONFIG['path'], task='pose')
            
            # Define os parâmetros de detecção
            self.hand_raise_threshold = GESTURE_CONFIG['hand_raise_threshold']
            self.min_confidence = GESTURE_CONFIG['min_detection_confidence']
            
        except Exception as e:
            raise RuntimeError(f"Erro ao inicializar detector: {e}")

    def detect(self, frame):
        """
        Detecta pessoas com as mãos levantadas no frame
        
        Args:
            frame (numpy.ndarray): Frame para análise
            
        Returns:
            list: Lista de detecções com bounding boxes e pontos-chave
        """
        if frame is None:
            return []
            
        results = self.model(frame, verbose=False)
        detections = []
        
        # Processa cada detecção do modelo
        for result in results:
            if not result.keypoints:
                continue
                
            keypoints = result.keypoints.xy[0].cpu().numpy()
            boxes = result.boxes
            
            # Analisa cada pessoa detectada
            for i, box in enumerate(boxes):
                if self._check_raised_hand(keypoints[i]):
                    confidence = float(box.conf[0].cpu().numpy())
                    
                    if confidence >= self.min_confidence:
                        x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                        detections.append({
                            'bbox': (x1, y1, x2, y2),
                            'keypoints': keypoints[i],
                            'confidence': confidence
                        })
        
        return detections

    def _check_raised_hand(self, keypoints):
        """
        Verifica se uma pessoa está com a mão levantada
        
        Args:
            keypoints (numpy.ndarray): Pontos-chave da pessoa
            
        Returns:
            bool: True se a pessoa estiver com a mão levantada
        """
        NOSE = 0
        LEFT_WRIST = 9
        RIGHT_WRIST = 10
        
        # Verifica se os pontos necessários foram detectados
        if not (keypoints[NOSE].any() and 
                (keypoints[LEFT_WRIST].any() or keypoints[RIGHT_WRIST].any())):
            return False
            
        nose_y = keypoints[NOSE][1]
        threshold = nose_y - (self.hand_raise_threshold * abs(keypoints[RIGHT_WRIST][1] - keypoints[LEFT_WRIST][1]))
        
        left_raised = (keypoints[LEFT_WRIST].any() and keypoints[LEFT_WRIST][1] < threshold)
        right_raised = (keypoints[RIGHT_WRIST].any() and keypoints[RIGHT_WRIST][1] < threshold)
        
        return left_raised or right_raised