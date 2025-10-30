from ultralytics import YOLO
import numpy as np

class GestureDetector:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)
        self.raised_hand_threshold = 0.7

    def detect_raised_hands(self, frame):
        results = self.model(frame)
        detections = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                if box.cls[0] == 0:  # pessoa
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = float(box.conf[0].cpu().numpy())
                    if self._is_hand_raised(box):
                        detections.append({
                            'bbox': (int(x1), int(y1), int(x2), int(y2)),
                            'confidence': conf
                        })
        
        return detections

    def _is_hand_raised(self, box):
        # Implementar lógica para detectar braço levantado
        # usando proporções do boundingbox ou pose estimation
        return True