def creaBombilla(nombre="Bombilla_1"):

    return {
        'nombre': nombre,
        'encendida': False,
        'intensidad': 0,
        'color' : {
            'r': 255,
            'g': 255,
            'b': 255
        }
    }

def encenderBombilla(bombilla):
    bombilla['encendida'] = True

    if bombilla['intensidad'] == 0:
        bombilla['intensidad'] = 100

def apagarBombilla(bombilla):
    bombilla['encendida'] = False
    bombilla['intensidad'] = 0

def obtenerEstado(bombilla):
    estado = "ENCENDIDA" if bombilla['encendida'] else "APAGADA"
    return f"Bombilla '{bombilla['nombre']}': {estado}, Intensidad: {bombilla['intensidad']}%, Color: RGB({bombilla['color']['r']}, {bombilla['color']['g']}, {bombilla['color']['b']})"

def cambiarIntensidad(bombilla, nivel):
    if 0 <= nivel <= 100:
        bombilla['intensidad'] = nivel
        return True
    else:
        print("Error: Intensidad debe estar entre 0 y 100")
        return False

def cambiarColor(bombilla, r, g, b):
    if all(0 <= valor <= 255 for valor in [r, g, b]):
        bombilla['color']['r'] = r
        bombilla['color']['g'] = g
        bombilla['color']['b'] = b
        return True
    else:
        print("Error: Color debe estar entre 0 y 255")
        return False

def imprimirBombilla(bombilla):
    print("=" * 40)
    print(f"BOMBILLA: {bombilla['nombre']}")
    print(f"Estado: {'ENCENDIDA' if bombilla['encendida'] else 'APAGADA'}")
    print(f"Intensidad: {bombilla['intensidad']}%")
    print(f"Color RGB: ({bombilla['color']['r']}, {bombilla['color']['g']}, {bombilla['color']['b']})")
    print("=" * 40)
