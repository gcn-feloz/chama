import time
from datetime import datetime
from config import ALERT_CONFIGS

class AlertSystem:
    def __init__(self):
        """
        Inicializa o sistema de alertas
        """
        self.active_alerts = {}
        self.alert_timeout = ALERT_CONFIGS['timeout']
        self.min_confidence = ALERT_CONFIGS['min_confidence']

    def process_detections(self, detections):
        """
        Processa as detecções e gera alertas
        Args:
            detections: Lista de detecções com informações das zonas
        Returns:
            list: Lista de alertas ativos
        """
        current_time = time.time()
        alerts = []

        for detection in detections:
            table_name = detection['table']
            
            if table_name not in self.active_alerts:
                self.active_alerts[table_name] = {
                    'timestamp': current_time,
                    'location': detection['detection']['bbox'],
                    'table': table_name
                }
                alerts.append({
                    'table': table_name,
                    'time': datetime.fromtimestamp(current_time).strftime('%H:%M:%S'),
                    'status': 'NOVO'
                })
            
        self._cleanup_old_alerts(current_time)
        return alerts

    def _cleanup_old_alerts(self, current_time):
        """
        Remove alertas que expiraram
        Args:
            current_time: Tempo atual em segundos
        """
        expired = []
        for alert_id, data in self.active_alerts.items():
            if current_time - data['timestamp'] > self.alert_timeout:
                expired.append(alert_id)
        
        for alert_id in expired:
            del self.active_alerts[alert_id]
            
    def clear_alerts(self):
        """
        Limpa todos os alertas ativos
        """
        self.active_alerts.clear()