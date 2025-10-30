# Configurações globais da aplicação

# Configurações de vídeo
VIDEO_CONFIGS = {
    'youtube_url': 'https://www.youtube.com/watch?v=2sHUoP0WqGk',
    'camera_id': 0,  # 0 para webcam padrão
    'use_youtube': True  # True para usar YouTube, False para usar câmera local
}

# Configurações do modelo
MODEL_CONFIGS = {
    'model_path': 'yolov8n.pt',
    'confidence_threshold': 0.5,
    'nms_threshold': 0.45
}

# Configurações de exibição
DISPLAY_CONFIGS = {
    'window_name': 'CHAMA - Detector',
    'font_scale': 0.5,
    'thickness': 2
}

# Configurações do sistema de alertas
ALERT_CONFIGS = {
    'timeout': 30,  # segundos
    'min_confidence': 0.7
}