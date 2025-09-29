from aire_acondicionado_adt import *

def main():
    print("=== PRUEBAS DE VALIDACIÓN HU02 ===\n")

    # Crear aire acondicionado
    aire = crearAireAcondicionado()
    print("1. CREACIÓN:")
    imprimirAire(aire)

    # Test encender
    print("2. ENCENDER:")
    encenderAire(aire)
    imprimirAire(aire)

    # Test cambiar temperatura a 21 grados
    print("3. CAMBIAR TEMPERATURA (21°C):")
    cambiarTemperatura(aire, 21)
    imprimirAire(aire)

    # Test obtener estado
    print("4. OBTENER ESTADO:")
    print(obtenerEstadoAire(aire))

    # Test apagar
    print("\n5. APAGAR:")
    apagarAire(aire)
    imprimirAire(aire)

if __name__ == "__main__":
    main()
