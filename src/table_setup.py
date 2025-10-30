import cv2
import json
import numpy as np
from stream_capture import StreamCapture

class TableSetup:
    def __init__(self):
        self.zones = []
        self.current_points = []
        self.drawing = False
        
    def setup_tables(self):
        stream = StreamCapture()
        frame = stream.get_frame()
        if frame is None:
            print("Erro ao capturar frame inicial")
            return
            
        cv2.namedWindow("Table Setup")
        cv2.setMouseCallback("Table Setup", self._mouse_callback)
        
        while True:
            display_frame = frame.copy()
            
            # Desenha zonas existentes
            for i, zone in enumerate(self.zones):
                pt1, pt2 = zone
                cv2.rectangle(display_frame, pt1, pt2, (0, 255, 0), 2)
                cv2.putText(display_frame, f"Mesa {i+1}", pt1, 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
            # Desenha zona atual sendo criada
            if len(self.current_points) == 1:
                cv2.circle(display_frame, self.current_points[0], 3, (0, 0, 255), -1)
                
            cv2.imshow("Table Setup", display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                self._save_zones()
                break
                
        cv2.destroyAllWindows()
        stream.release()
        
    def _mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.current_points) == 0:
                self.current_points.append((x, y))
            elif len(self.current_points) == 1:
                self.zones.append((self.current_points[0], (x, y)))
                self.current_points = []
                
    def _save_zones(self):
        config = {
            "tables": [
                {
                    "id": i + 1,
                    "name": f"Mesa {i + 1}",
                    "coordinates": [
                        list(zone[0]),
                        list(zone[1])
                    ]
                }
                for i, zone in enumerate(self.zones)
            ]
        }
        
        with open('table_zones.json', 'w') as f:
            json.dump(config, f, indent=4)
            
        print("Configuração das mesas salva com sucesso!")