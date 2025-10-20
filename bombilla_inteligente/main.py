from bombilla_adt import BombillaInteligente

def main():
    print("=== PRUEBAS DE VALIDACIÓN HU01 ===\n")

    # Crear bombilla
    bombilla = BombillaInteligente("Bombilla_Salon")
    print("1. CREACIÓN:")
    print(bombilla)

    # Test encender
    print("2. ENCENDER:")
    bombilla.encender()
    print(bombilla)

    # Test cambiar intensidad
    print("3. CAMBIAR INTENSIDAD (50%):")
    bombilla.cambiar_intensidad(50)
    print(bombilla)

    # Test cambiar color (rojo)
    print("4. CAMBIAR COLOR (ROJO):")
    bombilla.cambiar_color(255, 0, 0)
    print(bombilla)

    # Test obtener estado
    print("5. OBTENER ESTADO:")
    print(bombilla.obtener_estado())

    # Test apagar
    print("\n6. APAGAR:")
    bombilla.apagar()
    print(bombilla)


if __name__ == "__main__":
    main()
