from bombilla_adt import *

def main():
    print("=== PRUEBAS DE VALIDACIÓN HU01 ===\n")

    # Crear bombilla
    bombilla = creaBombilla("Bombilla_Salon")
    print("1. CREACIÓN:")
    imprimirBombilla(bombilla)

    # Test encender
    print("2. ENCENDER:")
    encenderBombilla(bombilla)
    imprimirBombilla(bombilla)

    # Test cambiar intensidad
    print("3. CAMBIAR INTENSIDAD (50%):")
    cambiarIntensidad(bombilla, 50)
    imprimirBombilla(bombilla)

    # Test cambiar color (rojo)
    print("4. CAMBIAR COLOR (ROJO):")
    cambiarColor(bombilla, 255, 0, 0)
    imprimirBombilla(bombilla)

    # Test obtener estado
    print("5. OBTENER ESTADO:")
    print(obtenerEstado(bombilla))

    # Test apagar
    print("\n6. APAGAR:")
    apagarBombilla(bombilla)
    imprimirBombilla(bombilla)


if __name__ == "__main__":
    main()
