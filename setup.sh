#!/bin/bash

# Ativa o ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Instala dependências necessárias
pip install torch==2.0.1 torchvision==0.15.2
pip install ultralytics==8.0.196
pip install yt-dlp==2023.10.13
pip install opencv-python
pip install pygame

echo "Instalação concluída! Execute com: python3 src/__init__.py"