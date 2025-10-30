# Configurações globais da aplicação

# Configurações de vídeo e performance
VIDEO_CONFIGS = {
    'youtube_url': 'https://www.youtube.com/watch?v=2sHUoP0WqGk',
    'camera_id': 0,  # 0 para webcam padrão
    'use_youtube': True,  # True para usar YouTube, False para usar câmera local
    'frame_width': 640,   # Largura do frame processado
    'frame_height': 480,  # Altura do frame processado
    'target_fps': 30,     # FPS alvo para processamento
    'skip_frames': 10      # Pula frames para melhorar performance (1 = processa todos)
}

# Configurações do modelo
MODEL_CONFIGS = {
    'model_path': 'yolov8n-pose.pt',  # Modelo para pose estimation
    'confidence_threshold': 0.5,
    'nms_threshold': 0.45,
    'classes': [0],  # Apenas pessoas
    'device': 'cpu',  # ou 'cuda' se tiver GPU
    'verbose': False  # Desabilita mensagens de detecção
}

# Configurações de exibição
DISPLAY_CONFIGS = {
    'window_name': 'CHAMA - Detector',
    'window_width': 640,    # Largura da janela de exibição
    'window_height': 480,   # Altura da janela de exibição
    'font_scale': 0.5,
    'thickness': 2,
    'show_fps': True       # Mostra FPS na tela
}

# Configurações de alerta
ALERT_CONFIGS = {
    'timeout': 30,         # segundos para um alerta expirar
    'min_confidence': 0.7, # confiança mínima para gerar alerta
    'sound_file': 'sino.wav',  # nome do arquivo de som
    'sound_interval': 5,   # intervalo entre repetições do som
    'sound_volume': 0.5    # volume do som (0.0 a 1.0)
}