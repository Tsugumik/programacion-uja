from aire_acondicionado.aire_acondicionado_adt import AireAcondicionado
from bombilla_inteligente.bombilla_adt import BombillaInteligente
from distribucion_hogar_adt import Hogar

def main():
    print("=== PRUEBAS DE VALIDACIÓN HU03 ===\n")

    # Crear hogar
    hogar = Hogar()
    print("1. CREACIÓN HOGAR:")
    print(f"Habitaciones: {hogar.obtener_habitaciones()}")
    print(f"Dispositivos: {hogar.obtener_dispositivos()}\n")

    # Añadir habitaciones
    print("2. AÑADIR HABITACIONES:")
    hogar.anadir_habitacion("Salon")
    hogar.anadir_habitacion("Dormitorio")
    print(f"Habitaciones: {hogar.obtener_habitaciones()}\n")

    # Crear dispositivos
    bombilla = BombillaInteligente("Bombilla_Salon")
    aire = AireAcondicionado()

    # Añadir dispositivos al hogar
    print("3. AÑADIR DISPOSITIVOS:")
    hogar.anadir_dispositivo("b1", bombilla, "Salon")
    hogar.anadir_dispositivo("a1", aire, "Dormitorio")
    print(f"Dispositivos: {hogar.obtener_dispositivos()}\n")

    # Contar dispositivos
    print("4. CONTAR DISPOSITIVOS:")
    print(f"Total: {hogar.contar_dispositivos()}")
    print(f"En Salon: {hogar.contar_dispositivos_por_habitacion('Salon')}")
    print(f"En Dormitorio: {hogar.contar_dispositivos_por_habitacion('Dormitorio')}\n")

    # Identificar ubicación
    print("5. IDENTIFICAR UBICACIÓN DISPOSITIVOS:")
    print(f"Dispositivo 'b1' en: {hogar.identificar_dispositivo_ubicacion('b1')}")
    print(f"Dispositivo 'a1' en: {hogar.identificar_dispositivo_ubicacion('a1')}\n")

    # Modificar dispositivo (ejemplo cambiar intensidad bombilla y temperatura aire)
    print("6. MODIFICAR DISPOSITIVOS:")
    hogar.modificar_dispositivo('b1', 'intensidad', 75)
    hogar.modificar_dispositivo('a1', 'temperatura', 20)
    print("Estado bombilla 'b1':")
    print(hogar.dispositivos['b1']['objeto'])
    print("Estado aire acondicionado 'a1':")
    print(hogar.dispositivos['a1']['objeto'])
    print()

    # Quitar dispositivo
    print("7. QUITAR DISPOSITIVO 'b1':")
    hogar.quitar_dispositivo('b1')
    print(f"Dispositivos: {hogar.obtener_dispositivos()}")
    print(f"Total: {hogar.contar_dispositivos()}")

if __name__ == "__main__":
    main()
