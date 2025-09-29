def crearHogar():
    return {
        'habitaciones': [],
        'dispositivos': {}
    }

def añadirHabitacion(hogar, nombre_habitacion):
    if nombre_habitacion not in hogar['habitaciones']:
        hogar['habitaciones'].append(nombre_habitacion)
        return True
    else:
        print(f"La habitación '{nombre_habitacion}' ya existe.")
        return False

def obtenerHabitaciones(hogar):
    return hogar['habitaciones']

def añadirDispositivo(hogar, dispositivo_id, dispositivo_objeto, habitacion):
    if habitacion not in hogar['habitaciones']:
        print(f"No existe la habitación '{habitacion}'.")
        return False
    hogar['dispositivos'][dispositivo_id] = {
        'objeto': dispositivo_objeto,
        'habitacion': habitacion
    }
    return True

def quitarDispositivo(hogar, dispositivo_id):
    if dispositivo_id in hogar['dispositivos']:
        del hogar['dispositivos'][dispositivo_id]
        return True
    else:
        print(f"No existe el dispositivo '{dispositivo_id}'.")
        return False

def modificarDispositivo(hogar, dispositivo_id, propiedad, valor):
    if dispositivo_id in hogar['dispositivos']:
        dispositivo = hogar['dispositivos'][dispositivo_id]['objeto']
        if hasattr(dispositivo, propiedad) or propiedad in dispositivo:
            dispositivo[propiedad] = valor
            return True
        else:
            print(f"La propiedad '{propiedad}' no existe en el dispositivo.")
            return False
    else:
        print(f"No existe el dispositivo '{dispositivo_id}'.")
        return False

def contarDispositivos(hogar):
    return len(hogar['dispositivos'])

def contarDispositivosPorHabitacion(hogar, habitacion):
    count = 0
    for disp in hogar['dispositivos'].values():
        if disp['habitacion'] == habitacion:
            count += 1
    return count

def identificarDispositivoUbicacion(hogar, dispositivo_id):
    if dispositivo_id in hogar['dispositivos']:
        return hogar['dispositivos'][dispositivo_id]['habitacion']
    else:
        return None

def obtenerDispositivos(hogar):
    return list(hogar['dispositivos'].keys())
