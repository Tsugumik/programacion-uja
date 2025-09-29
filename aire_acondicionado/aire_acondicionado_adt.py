def crearAireAcondicionado():
    return {
        'temperatura': 24.0,
        'encendido': False
    }


def encenderAire(aire):
    aire['encendido'] = True


def apagarAire(aire):
    aire['encendido'] = False


def obtenerEstadoAire(aire):
    estado = "ENCENDIDO" if aire['encendido'] else "APAGADO"
    return f"Aire acondicionado está {estado}, Temperatura: {aire['temperatura']}°C"


def cambiarTemperatura(aire, nueva_temperatura):
    if 16 <= nueva_temperatura <= 30:
        aire['temperatura'] = nueva_temperatura
        return True
    else:
        print("Error: La temperatura debe estar entre 16 y 30 grados Celsius.")
        return False


def imprimirAire(aire):
    print("=" * 40)
    print("CLIMATIZADOR")
    print(f"Estado: {'ENCENDIDO' if aire['encendido'] else 'APAGADO'}")
    print(f"Temperatura: {aire['temperatura']}°C")
    print("=" * 40)
