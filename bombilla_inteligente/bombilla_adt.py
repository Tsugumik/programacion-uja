class BombillaInteligente:
    def __init__(self, nombre="Bombilla_1"):
        self.nombre = nombre
        self.encendida = False
        self.intensidad = 0
        self.color = {'r': 255, 'g': 255, 'b': 255}

    def encender(self):
        self.encendida = True
        if self.intensidad == 0:
            self.intensidad = 100

    def apagar(self):
        self.encendida = False
        self.intensidad = 0

    def obtener_estado(self):
        estado = "ENCENDIDA" if self.encendida else "APAGADA"
        return f"Bombilla '{self.nombre}': {estado}, Intensidad: {self.intensidad}%, Color: RGB({self.color['r']}, {self.color['g']}, {self.color['b']})"

    def cambiar_intensidad(self, nivel):
        if 0 <= nivel <= 100:
            self.intensidad = nivel
            return True
        else:
            print("Error: Intensidad debe estar entre 0 y 100")
            return False

    def cambiar_color(self, r, g, b):
        if all(0 <= valor <= 255 for valor in [r, g, b]):
            self.color['r'] = r
            self.color['g'] = g
            self.color['b'] = b
            return True
        else:
            print("Error: Color debe estar entre 0 y 255")
            return False

    def __str__(self):
        header = "=" * 40
        estado_str = 'ENCENDIDA' if self.encendida else 'APAGADA'
        return (f"{header}\n"
                f"BOMBILLA: {self.nombre}\n"
                f"Estado: {estado_str}\n"
                f"Intensidad: {self.intensidad}%\n"
                f"Color RGB: ({self.color['r']}, {self.color['g']}, {self.color['b']})\n"
                f"{header}")
