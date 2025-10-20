class Hogar:
    def __init__(self):
        self.habitaciones = []
        self.dispositivos = {}

    def anadir_habitacion(self, nombre_habitacion):
        if nombre_habitacion not in self.habitaciones:
            self.habitaciones.append(nombre_habitacion)
            return True
        else:
            print(f"La habitación '{nombre_habitacion}' ya existe.")
            return False

    def obtener_habitaciones(self):
        return self.habitaciones

    def anadir_dispositivo(self, dispositivo_id, dispositivo_objeto, habitacion):
        if habitacion not in self.habitaciones:
            print(f"No existe la habitación '{habitacion}'.")
            return False
        self.dispositivos[dispositivo_id] = {
            'objeto': dispositivo_objeto,
            'habitacion': habitacion
        }
        return True

    def quitar_dispositivo(self, dispositivo_id):
        if dispositivo_id in self.dispositivos:
            del self.dispositivos[dispositivo_id]
            return True
        else:
            print(f"No existe el dispositivo '{dispositivo_id}'.")
            return False

    def modificar_dispositivo(self, dispositivo_id, propiedad, valor):
        if dispositivo_id in self.dispositivos:
            dispositivo = self.dispositivos[dispositivo_id]['objeto']
            if hasattr(dispositivo, propiedad):
                setattr(dispositivo, propiedad, valor)
                return True
            else:
                print(f"La propiedad '{propiedad}' no existe en el dispositivo.")
                return False
        else:
            print(f"No existe el dispositivo '{dispositivo_id}'.")
            return False

    def contar_dispositivos(self):
        return len(self.dispositivos)

    def contar_dispositivos_por_habitacion(self, habitacion):
        count = 0
        for disp in self.dispositivos.values():
            if disp['habitacion'] == habitacion:
                count += 1
        return count

    def identificar_dispositivo_ubicacion(self, dispositivo_id):
        if dispositivo_id in self.dispositivos:
            return self.dispositivos[dispositivo_id]['habitacion']
        else:
            return None

    def obtener_dispositivos(self):
        return list(self.dispositivos.keys())
