import json

class ServicioUsuarios:
    def __init__(self):
        self.db_file = "db_usuarios.json"

    def obtener_usuario(self, nombre):
        print("[Servicio Usuarios] Consultando usuario...")
        usuarios = self._leer_db()

        for u in usuarios:
            if u["nombre"] == nombre:
                return u["nombre"]

        return "Usuario desconocido"

    def _leer_db(self):
        try:
            with open(self.db_file, "r") as f:
                print("[DB Usuarios] Leyendo archivo JSON")
                return json.load(f)
        except:
            return []