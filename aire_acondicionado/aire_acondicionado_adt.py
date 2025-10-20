class AireAcondicionado:
    def __init__(self):
        self.temperatura = 24.0
        self.encendido = False

    def encender(self):
        self.encendido = True

    def apagar(self):
        self.encendido = False

    def obtener_estado(self):
        estado = "ENCENDIDO" if self.encendido else "APAGADO"
        return f"Aire acondicionado está {estado}, Temperatura: {self.temperatura}°C"

    def cambiar_temperatura(self, nueva_temperatura):
        if 16 <= nueva_temperatura <= 30:
            self.temperatura = nueva_temperatura
            return True
        else:
            print("Error: La temperatura debe estar entre 16 y 30 grados Celsius.")
            return False

    def __str__(self):
        header = "=" * 40
        estado_str = 'ENCENDIDO' if self.encendido else 'APAGADO'
        return (f"{header}\n"
                f"CLIMATIZADOR\n"
                f"Estado: {estado_str}\n"
                f"Temperatura: {self.temperatura}°C\n"
                f"{header}")
