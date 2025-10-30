"""
Módulo principal da aplicação.
"""
import cv2
import yt_dlp
import pygame
from ultralytics import YOLO
from config import VIDEO_URL, VIDEO_CONFIG, MODEL_CONFIG, SOUND_CONFIG

def get_youtube_url():
    """Obtém a URL do stream do vídeo do YouTube"""
    try:
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(VIDEO_URL, download=False)
            return info['url']
    except Exception as e:
        print(f"Erro ao obter URL do YouTube: {e}")
        return None

def main():
    cap = None
    try:
        # Inicializa som
        pygame.mixer.init()
        sound = pygame.mixer.Sound(SOUND_CONFIG['file'])
        sound.set_volume(SOUND_CONFIG['volume'])
        sound_playing = False
        
        # Carrega modelo YOLO
        print("Carregando modelo...")
        model = YOLO(MODEL_CONFIG['path'])
        
        # Configura vídeo do YouTube
        print("Conectando ao vídeo...")
        video_url = get_youtube_url()
        if not video_url:
            raise RuntimeError("Não foi possível obter URL do vídeo")
            
        cap = cv2.VideoCapture(video_url)
        if not cap.isOpened():
            raise RuntimeError("Não foi possível abrir o vídeo")
        
        print("\nControles:")
        print("'q' - Sair")
        print("'a' - Desativar alarme\n")
        
        # Loop principal
        while True:
            # Lê frame
            ret, frame = cap.read()
            if not ret:
                print("Fim do vídeo ou erro na leitura")
                break
                
            # Redimensiona frame
            frame = cv2.resize(frame, (VIDEO_CONFIG['width'], VIDEO_CONFIG['height']))
            
            # Detecta pessoas
            results = model(frame, verbose=False)
            
            alerta = False
            # Para cada pessoa detectada
            for result in results:
                if result.keypoints is None:
                    continue
                    
                keypoints = result.keypoints.xy[0].cpu().numpy()
                boxes = result.boxes
                
                for i, box in enumerate(boxes):
                    # Verifica se tem confiança suficiente
                    conf = float(box.conf[0].cpu().numpy())
                    if conf < MODEL_CONFIG['conf']:
                        continue
                        
                    # Pega os pontos-chave relevantes
                    nose = keypoints[i][0]  # nariz
                    left_wrist = keypoints[i][9]  # pulso esquerdo
                    right_wrist = keypoints[i][10]  # pulso direito
                    
                    # Se os pontos foram detectados
                    if nose.any() and (left_wrist.any() or right_wrist.any()):
                        nose_y = nose[1]
                        
                        # Verifica se algum pulso está acima do nariz
                        if ((left_wrist.any() and left_wrist[1] < nose_y) or
                            (right_wrist.any() and right_wrist[1] < nose_y)):
                                
                            # Desenha retângulo na pessoa
                            x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            
                            # Marca que tem alerta
                            alerta = True
            
            # Atualiza som
            if alerta and not sound_playing:
                sound.play(-1)
                sound_playing = True
            elif not alerta and sound_playing:
                sound.stop()
                sound_playing = False
            
            # Mostra frame
            cv2.imshow("CHAMA - Detector", frame)
            
            # Processa teclas
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('a'):
                sound.stop()
                sound_playing = False
                
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        # Limpa recursos
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()