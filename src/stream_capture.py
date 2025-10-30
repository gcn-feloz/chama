import cv2
import subprocess

def get_stream_url(youtube_url: str) -> str:
    """
    Usa o yt-dlp para obter o link direto (m3u8) do stream do YouTube.
    """
    try:
        # Executa o comando yt-dlp -g e captura o link
        result = subprocess.run(
            ["yt-dlp", "-g", youtube_url],
            capture_output=True,
            text=True,
            check=True
        )
        stream_url = result.stdout.strip()
        print(f"[INFO] URL do stream obtida:\n{stream_url}\n")
        return stream_url
    except subprocess.CalledProcessError as e:
        print("[ERRO] Falha ao obter o link do stream.")
        print(e.stderr)
        return None


def stream_video(stream_url: str):
    """
    Lê o vídeo diretamente via OpenCV e exibe os frames.
    """
    cap = cv2.VideoCapture(stream_url)

    if not cap.isOpened():
        print("[ERRO] Não foi possível abrir o stream.")
        return

    print("[INFO] Stream iniciado. Pressione 'q' para sair.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[AVISO] Falha ao ler frame. Tentando novamente...")
            break

        cv2.imshow("Chama - Stream ao vivo", frame)

        # Pressione 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Stream encerrado.")


if __name__ == "__main__":
    YOUTUBE_URL = "https://www.youtube.com/watch?v=2sHUoP0WqGk"
    url = get_stream_url(YOUTUBE_URL)
    if url:
        stream_video(url)