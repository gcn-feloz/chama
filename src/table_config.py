class TableZone:
    def __init__(self, id, coordinates, name=""):
        self.id = id
        self.coordinates = coordinates  # [(x1,y1), (x2,y2)] - pontos para criar retângulo
        self.name = name or f"Mesa {id}"
        self.is_active = False
        self.last_detection_time = None

# Configuração das zonas das mesas
TABLE_ZONES = [
    TableZone(1, [(100, 100), (200, 200)], "Mesa 1"),
    TableZone(2, [(250, 100), (350, 200)], "Mesa 2"),
    TableZone(3, [(400, 100), (500, 200)], "Mesa 3"),
    # Adicione mais mesas conforme necessário
]