"""
Módulo de alertas sonoros.
Gerencia a reprodução de sons de alerta.
"""
import pygame
import os
from config import AUDIO_CONFIG

class AudioAlert:
    def __init__(self):
        """Inicializa o sistema de áudio"""
        pygame.mixer.init()
        sound_path = AUDIO_CONFIG['sound_file']
        
        if not os.path.exists(sound_path):
            raise FileNotFoundError(f"Arquivo de som não encontrado: {sound_path}")
            
        self.sound = pygame.mixer.Sound(sound_path)
        self.sound.set_volume(AUDIO_CONFIG['volume'])
        self.playing = False
        self.last_play = 0

    def play(self):
        """Inicia a reprodução do som de alerta"""
        if not self.playing:
            self.sound.play(-1)  # -1 indica loop infinito
            self.playing = True

    def stop(self):
        """Para a reprodução do som de alerta"""
        if self.playing:
            self.sound.stop()
            self.playing = False