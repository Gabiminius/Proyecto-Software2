import json

class AlmacenamientoDocumentos:
    def __init__(self):
        self.db_file = "documentos.json"

    def guardar_documento(self, incidente):
        print("[Almacenamiento Documentos] Guardando documento adjunto...")
        docs = self._leer_db()
        docs.append({"incidente": incidente["descripcion"]})
        self._guardar_db(docs)

    def _leer_db(self):
        try:
            with open(self.db_file, "r") as f:
                print("[Documentos] Leyendo archivo JSON")
                return json.load(f)
        except:
            return []

    def _guardar_db(self, data):
        with open(self.db_file, "w") as f:
            print("[Documentos] Escribiendo archivo JSON")
            json.dump(data, f, indent=2)