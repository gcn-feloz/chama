import cv2
import yt_dlp
from config import VIDEO_CONFIGS

class StreamCapture:
    def __init__(self):
        """
        Inicializa a captura de vídeo baseada nas configurações globais
        """
        self.use_youtube = VIDEO_CONFIGS['use_youtube']
        
        if self.use_youtube:
            url = VIDEO_CONFIGS['youtube_url']
            video_url = self._get_youtube_stream_url(url)
            self.capture = cv2.VideoCapture(video_url)
        else:
            self.capture = cv2.VideoCapture(VIDEO_CONFIGS['camera_id'])
    
    def _get_youtube_stream_url(self, url):
        """
        Obtém a URL do stream do YouTube usando yt-dlp
        """
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['url']

    def get_frame(self):
        """
        Captura e retorna o próximo frame do vídeo
        """
        if not self.capture.isOpened():
            return None
            
        ret, frame = self.capture.read()
        if not ret:
            return None
            
        return frame
        
    def release(self):
        """
        Libera os recursos de captura de vídeo
        """
        if self.capture:
            self.capture.release()