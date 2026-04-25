class ServicioAutenticacion:
    def validar_token(self, token):
        print("[Servicio Autenticación] Validando token...")

        if token == "fake-token":
            print("[Servicio Autenticación] Token válido")
            return True
        else:
            print("[Servicio Autenticación] Token inválido")
            return False