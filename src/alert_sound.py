import pygame
import time
from threading import Thread
from config import ALERT_CONFIGS

class AlertSound:
    def __init__(self):
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(ALERT_CONFIGS['sound_file'])
        self.playing = False
        self.sound_thread = None
        
    def start_alert(self):
        if not self.playing:
            self.playing = True
            self.sound_thread = Thread(target=self._play_loop)
            self.sound_thread.daemon = True
            self.sound_thread.start()
    
    def stop_alert(self):
        self.playing = False
        if self.sound_thread:
            self.sound_thread.join()
    
    def _play_loop(self):
        while self.playing:
            self.sound.play()
            time.sleep(ALERT_CONFIGS['sound_interval'])