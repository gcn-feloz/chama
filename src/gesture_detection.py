from ultralytics import YOLO
import numpy as np

class GestureDetector:
    def __init__(self):
        """
        Inicializa o detector de gestos
        Utiliza o modelo YOLOv8-pose para detectar pontos-chave do corpo
        """
        self.model = YOLO('yolov8n-pose.pt')  # Modelo específico para pose estimation
        self.model.predictor.args.verbose = False  # Desabilita mensagens
        self.raised_hand_threshold = 0.3  # Diferença vertical mínima para considerar braço levantado
        
    def detect_raised_hands(self, frame):
        """
        Detecta pessoas com as mãos levantadas no frame
        Args:
            frame: Frame do vídeo para análise
        Returns:
            list: Lista de detecções de pessoas com mãos levantadas
        """
        results = self.model(frame)
        detections = []
        
        for result in results:
            if not result.keypoints:  # Pula se não houver keypoints
                continue
                
            keypoints = result.keypoints.xy[0].cpu().numpy()  # Extrai pontos-chave
            boxes = result.boxes
            
            for i, box in enumerate(boxes):
                if self._is_hand_raised(keypoints[i]):
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = float(box.conf[0].cpu().numpy())
                    detections.append({
                        'bbox': (int(x1), int(y1), int(x2), int(y2)),
                        'confidence': conf
                    })
        
        return detections

    def _is_hand_raised(self, keypoints):
        """
        Verifica se a pessoa está com pelo menos um braço levantado
        Args:
            keypoints: Array numpy com os pontos-chave da pessoa
        Returns:
            bool: True se um braço estiver levantado
        """
        # Índices dos keypoints relevantes (no formato COCO)
        NOSE = 0
        LEFT_WRIST = 9
        RIGHT_WRIST = 10
        
        # Verifica se os pontos necessários foram detectados
        if not (keypoints[NOSE].any() and 
                (keypoints[LEFT_WRIST].any() or keypoints[RIGHT_WRIST].any())):
            return False
        
        nose_y = keypoints[NOSE][1]
        
        # Verifica se algum pulso está acima do nariz
        left_raised = (keypoints[LEFT_WRIST].any() and 
                      keypoints[LEFT_WRIST][1] < nose_y - self.raised_hand_threshold)
        right_raised = (keypoints[RIGHT_WRIST].any() and 
                       keypoints[RIGHT_WRIST][1] < nose_y - self.raised_hand_threshold)
        
        return left_raised or right_raised