from ultralytics import YOLO
import cv2
import numpy as np
from config import MODEL_CONFIGS, VIDEO_CONFIGS

class ObjectDetector:
    def __init__(self):
        """
        Inicializa o detector de objetos usando as configurações do config.py
        """
        self.model = YOLO(MODEL_CONFIGS['model_path'])
        # Configura para detectar apenas pessoas e desabilita mensagens
        self.model.predictor.args.classes = [0]  # 0 = pessoa na COCO dataset
        self.model.predictor.args.verbose = False
        self.conf_threshold = MODEL_CONFIGS['confidence_threshold']
        self.device = MODEL_CONFIGS['device']
        
    def detect(self, frame):
        """
        Realiza a detecção de pessoas no frame
        Args:
            frame (np.ndarray): Frame do vídeo para processar
        Returns:
            list: Lista de detecções de pessoas
        """
        if frame is None:
            return []
            
        results = self.model(frame)
        detections = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = box.conf[0].cpu().numpy()
                class_id = box.cls[0].cpu().numpy()
                
                detections.append({
                    'bbox': (int(x1), int(y1), int(x2), int(y2)),
                    'confidence': float(confidence),
                    'class_id': int(class_id)
                })
                
        return detections

def get_stream_url(youtube_url: str, quality_tag="93") -> str:
    """
    Obtém o link direto m3u8 em qualidade menor (padrão 640x360).
    """
    try:
        result = subprocess.run(
            ["yt-dlp", "-f", quality_tag, "-g", youtube_url],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("[ERRO] Falha ao obter o link do stream:", e.stderr)
        return None

def run_detection(youtube_url: str):
    stream_url = get_stream_url(youtube_url)
    if not stream_url:
        print("[ERRO] Nenhum URL obtido.")
        return

    print(f"[INFO] Iniciando stream com YOLO otimizado...\n{stream_url}\n")

    detector = ObjectDetector()

    # Limita o processamento para menor carga
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print("[ERRO] Falha ao abrir o vídeo.")
        return

    print("[INFO] Pressione 'q' para encerrar.")

    # Reduz frequência de processamento
    last_time = 0
    frame_interval = 1 / 2  # ~2 FPS

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[AVISO] Frame não lido, encerrando...")
            break

        now = time.time()
        if now - last_time > frame_interval:
            last_time = now

            # Redimensiona frame para aliviar CPU
            frame = cv2.resize(frame, (640, 360))

            detections = detector.detect(frame)
            for detection in detections:
                x1, y1, x2, y2 = detection['bbox']
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

            cv2.imshow("Chama - Detecção (modo leve)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Stream encerrado.")

if __name__ == "__main__":
    run_detection("https://www.youtube.com/watch?v=2sHUoP0WqGk")
