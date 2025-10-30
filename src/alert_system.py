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
        current_time = time.time()
        alerts = []

        for detection in detections:
            alert_id = f"table_{len(self.active_alerts) + 1}"
            
            if alert_id not in self.active_alerts:
                self.active_alerts[alert_id] = {
                    'timestamp': current_time,
                    'location': detection['bbox']
                }
                alerts.append({
                    'table': alert_id,
                    'time': datetime.fromtimestamp(current_time).strftime('%H:%M:%S'),
                    'status': 'NOVO'
                })
            
        self._cleanup_old_alerts(current_time)
        return alerts

    def _cleanup_old_alerts(self, current_time):
        expired = []
        for alert_id, data in self.active_alerts.items():
            if current_time - data['timestamp'] > self.alert_timeout:
                expired.append(alert_id)
        
        for alert_id in expired:
            del self.active_alerts[alert_id]