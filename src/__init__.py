from stream_capture import StreamCapture
from detection import ObjectDetector
from display import DisplayManager
from gesture_detection import GestureDetector
from alert_system import AlertSystem
from config import VIDEO_CONFIGS, MODEL_CONFIGS, DISPLAY_CONFIGS

def main():
    stream = StreamCapture()  # Não precisa mais passar a fonte de vídeo, pois já está em config.py
    detector = GestureDetector()
    alert_system = AlertSystem()
    display = DisplayManager()

    while True:
        frame = stream.get_frame()
        if frame is None:
            break

        # Detectar gestos
        detections = detector.detect_raised_hands(frame)
        
        # Processar alertas
        alerts = alert_system.process_detections(detections)
        
        # Exibir resultados
        display.show_frame(frame, detections, alerts)

if __name__ == '__main__':
    main()