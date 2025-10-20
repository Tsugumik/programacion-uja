from aire_acondicionado_adt import AireAcondicionado

def main():
    print("=== PRUEBAS DE VALIDACIÓN HU02 ===\n")

    # Crear aire acondicionado
    aire = AireAcondicionado()
    print("1. CREACIÓN:")
    print(aire)

    # Test encender
    print("2. ENCENDER:")
    aire.encender()
    print(aire)

    # Test cambiar temperatura a 21 grados
    print("3. CAMBIAR TEMPERATURA (21°C):")
    aire.cambiar_temperatura(21)
    print(aire)

    # Test obtener estado
    print("4. OBTENER ESTADO:")
    print(aire.obtener_estado())

    # Test apagar
    print("\n5. APAGAR:")
    aire.apagar()
    print(aire)

if __name__ == "__main__":
    main()
