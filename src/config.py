# Configurações globais da aplicação

# Configurações de vídeo e performance
VIDEO_CONFIGS = {
    'youtube_url': 'https://www.youtube.com/watch?v=2sHUoP0WqGk',
    'camera_id': 0,  # 0 para webcam padrão
    'use_youtube': True,  # True para usar YouTube, False para usar câmera local
    'frame_width': 640,   # Largura do frame processado
    'frame_height': 480,  # Altura do frame processado
    'target_fps': 15,     # FPS alvo para processamento
    'skip_frames': 2      # Pula frames para melhorar performance (1 = processa todos)
}

# Configurações do modelo
MODEL_CONFIGS = {
    'model_path': 'yolov8n.pt',  # Modelo mais leve do YOLOv8
    'confidence_threshold': 0.5,
    'nms_threshold': 0.45,
    'classes': [0],  # Apenas classe 0 (pessoa)
    'device': 'cpu'  # 'cpu' ou 'cuda' para GPU
}

# Configurações de exibição
DISPLAY_CONFIGS = {
    'window_name': 'CHAMA - Detector',
    'window_width': 800,    # Largura da janela de exibição
    'window_height': 600,   # Altura da janela de exibição
    'font_scale': 0.5,
    'thickness': 2,
    'show_fps': True       # Mostra FPS na tela
}

# Configurações de alerta
ALERT_CONFIGS = {
    'timeout': 30,         # Tempo em segundos para um alerta expirar
    'min_confidence': 0.7, # Confiança mínima para gerar alerta
    'sound_file': 'assets/ria.wav',  # Arquivo de som para alerta
    'sound_interval': 5    # Intervalo entre repetições do som (segundos)
}