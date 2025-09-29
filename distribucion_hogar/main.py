from aire_acondicionado.aire_acondicionado_adt import *
from bombilla_inteligente.bombilla_adt import *
from distribucion_hogar_adt import *

def main():
    print("=== PRUEBAS DE VALIDACIÓN HU03 ===\n")

    # Crear hogar
    hogar = crearHogar()
    print("1. CREACIÓN HOGAR:")
    print(f"Habitaciones: {obtenerHabitaciones(hogar)}")
    print(f"Dispositivos: {obtenerDispositivos(hogar)}\n")

    # Añadir habitaciones
    print("2. AÑADIR HABITACIONES:")
    añadirHabitacion(hogar, "Salon")
    añadirHabitacion(hogar, "Dormitorio")
    print(f"Habitaciones: {obtenerHabitaciones(hogar)}\n")

    # Crear dispositivos
    bombilla = creaBombilla("Bombilla_Salon")
    aire = crearAireAcondicionado()

    # Añadir dispositivos al hogar
    print("3. AÑADIR DISPOSITIVOS:")
    añadirDispositivo(hogar, "b1", bombilla, "Salon")
    añadirDispositivo(hogar, "a1", aire, "Dormitorio")
    print(f"Dispositivos: {obtenerDispositivos(hogar)}\n")

    # Contar dispositivos
    print("4. CONTAR DISPOSITIVOS:")
    print(f"Total: {contarDispositivos(hogar)}")
    print(f"En Salon: {contarDispositivosPorHabitacion(hogar, 'Salon')}")
    print(f"En Dormitorio: {contarDispositivosPorHabitacion(hogar, 'Dormitorio')}\n")

    # Identificar ubicación
    print("5. IDENTIFICAR UBICACIÓN DISPOSITIVOS:")
    print(f"Dispositivo 'b1' en: {identificarDispositivoUbicacion(hogar, 'b1')}")
    print(f"Dispositivo 'a1' en: {identificarDispositivoUbicacion(hogar, 'a1')}\n")

    # Modificar dispositivo (ejemplo cambiar intensidad bombilla y temperatura aire)
    print("6. MODIFICAR DISPOSITIVOS:")
    modificarDispositivo(hogar, 'b1', 'intensidad', 75)
    modificarDispositivo(hogar, 'a1', 'temperatura', 20)
    print("Estado bombilla 'b1':")
    imprimirBombilla(hogar['dispositivos']['b1']['objeto'])
    print("Estado aire acondicionado 'a1':")
    imprimirAire(hogar['dispositivos']['a1']['objeto'])
    print()

    # Quitar dispositivo
    print("7. QUITAR DISPOSITIVO 'b1':")
    quitarDispositivo(hogar, 'b1')
    print(f"Dispositivos: {obtenerDispositivos(hogar)}")
    print(f"Total: {contarDispositivos(hogar)}")

if __name__ == "__main__":
    main()
