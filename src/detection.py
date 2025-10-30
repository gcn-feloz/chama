import cv2
from ultralytics import YOLO
import subprocess
import time

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

    # YOLO mais leve
    model = YOLO("yolov8n.pt")

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

            results = model(frame, stream=True)
            for r in results:
                annotated = r.plot()
                cv2.imshow("Chama - Detecção (modo leve)", annotated)
                break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Stream encerrado.")

if __name__ == "__main__":
    run_detection("https://www.youtube.com/watch?v=2sHUoP0WqGk")
