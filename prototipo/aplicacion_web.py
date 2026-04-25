from api_gateway import APIGateway

class AplicacionWeb:
    def __init__(self):
        self.api = APIGateway()

    def ejecutar_demo(self):
        print("[Aplicación Web] Iniciando flujo de ejemplo...")

        incidente = {
            "profesor": "Juan Perez",
            "alumno": "Pedro Soto",
            "descripcion": "Interrupción en clase"
        }

        self.api.crear_incidente(incidente)