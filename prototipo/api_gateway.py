from servicio_incidentes import ServicioIncidentes
from servicio_autenticacion import ServicioAutenticacion

class APIGateway:
    def __init__(self):
        self.auth = ServicioAutenticacion()
        self.incidentes = ServicioIncidentes()

    def crear_incidente(self, data):
        print("[API Gateway] Recibiendo solicitud HTTP...")

        if self.auth.validar_token("fake-token"):
            print("[API Gateway] Token válido, enrutando a Servicio de Incidentes")
            self.incidentes.crear_incidente(data)
        else:
            print("[API Gateway] Token inválido")