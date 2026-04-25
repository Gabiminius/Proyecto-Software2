import json
from servicio_notificaciones import ServicioNotificaciones
from servicio_usuarios import ServicioUsuarios

from almacenamiento_documentos import AlmacenamientoDocumentos

class ServicioIncidentes:
    def __init__(self):
        self.notificaciones = ServicioNotificaciones()
        self.usuarios = ServicioUsuarios()
        self.documentos = AlmacenamientoDocumentos()
        self.db_file = "db_incidentes.json"

    def crear_incidente(self, data):
        print("[Servicio Incidentes] Procesando incidente...")

        incidentes = self._leer_db()
        incidentes.append(data)
        self._guardar_db(incidentes)

        print("[Servicio Incidentes] Incidente guardado")

        # Guardar documento simulado
        self.documentos.guardar_documento(data)

        usuario = self.usuarios.obtener_usuario(data["profesor"])
        self.notificaciones.notificar(usuario, data)

    def _leer_db(self):
        try:
            with open(self.db_file, "r") as f:
                print("[DB Incidentes] Leyendo archivo JSON")
                return json.load(f)
        except:
            return []

    def _guardar_db(self, data):
        with open(self.db_file, "w") as f:
            print("[DB Incidentes] Escribiendo archivo JSON")
            json.dump(data, f, indent=2)