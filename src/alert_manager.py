"""
Módulo do sistema de alertas.
Gerencia o estado dos alertas e suas transições.
"""
import time
from config import ALERT_CONFIG

class Alert:
    def __init__(self, table_id, table_name):
        """
        Inicializa um alerta para uma mesa específica
        
        Args:
            table_id: ID único da mesa
            table_name: Nome da mesa para exibição
        """
        self.table_id = table_id
        self.table_name = table_name
        self.state = ALERT_CONFIG['states']['inactive']
        self.last_detection = 0
        self.last_alert = 0
        self.detection_count = 0
        
    def update(self, detected):
        """
        Atualiza o estado do alerta baseado em uma nova detecção
        
        Args:
            detected: True se houve detecção, False caso contrário
            
        Returns:
            bool: True se o alerta está ativo
        """
        current_time = time.time()
        
        if detected:
            self.detection_count += 1
            self.last_detection = current_time
            
            # Se estiver inativo, muda para pendente
            if self.state == ALERT_CONFIG['states']['inactive']:
                self.state = ALERT_CONFIG['states']['pending']
                
            # Se pendente por tempo suficiente, ativa o alerta
            elif (self.state == ALERT_CONFIG['states']['pending'] and 
                  self.detection_count >= 3):
                self.state = ALERT_CONFIG['states']['active']
                self.last_alert = current_time
                
        else:
            # Reseta contagem se não houver detecção
            self.detection_count = 0
            
            # Se ativo por muito tempo, entra em cooldown
            if (self.state == ALERT_CONFIG['states']['active'] and 
                current_time - self.last_alert > ALERT_CONFIG['timeout']):
                self.state = ALERT_CONFIG['states']['cooldown']
                
            # Se em cooldown por tempo suficiente, volta a inativo
            elif (self.state == ALERT_CONFIG['states']['cooldown'] and 
                  current_time - self.last_alert > ALERT_CONFIG['min_interval']):
                self.state = ALERT_CONFIG['states']['inactive']
        
        return self.state == ALERT_CONFIG['states']['active']

class AlertManager:
    def __init__(self):
        """Inicializa o gerenciador de alertas"""
        self.alerts = {}
        
    def update(self, detections):
        """
        Atualiza o estado dos alertas com base nas detecções
        
        Args:
            detections: Lista de detecções com suas respectivas mesas
            
        Returns:
            list: Lista de alertas ativos
        """
        # Marca todas as mesas como não detectadas inicialmente
        detected_tables = {alert.table_id: False for alert in self.alerts.values()}
        
        # Processa as novas detecções
        for det in detections:
            table_id = det.get('table_id')
            table_name = det.get('table')
            
            if table_id and table_name:
                detected_tables[table_id] = True
                
                # Cria novo alerta se necessário
                if table_id not in self.alerts:
                    self.alerts[table_id] = Alert(table_id, table_name)
                    
        # Atualiza todos os alertas
        active_alerts = []
        for table_id, alert in self.alerts.items():
            if alert.update(detected_tables.get(table_id, False)):
                active_alerts.append({
                    'table_id': table_id,
                    'table': alert.table_name,
                    'state': alert.state
                })
                
        return active_alerts
        
    def clear(self):
        """Limpa todos os alertas ativos"""
        for alert in self.alerts.values():
            alert.state = ALERT_CONFIG['states']['inactive']
            alert.detection_count = 0