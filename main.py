from typing import List, Optional
from smart_home.home import Home
from smart_home.room import Room
from smart_home.device import Device
from smart_home.smart_bulb import SmartBulb
from smart_home.air_conditioner import AirConditioner
from smart_home.data_manager import DataManager
from smart_home.scheduler import Scheduler, InvalidTimeError

DATA_FILE = "home_data.json"
LOG_FILE = "room_history.log"

def select_room(home: Home) -> Optional[Room]:
    """Helper to select a room from the home."""
    rooms = home.rooms
    if not rooms:
        print("There are no rooms to select.")
        return None
    
    print("\nSelect a room:")
    for i, room in enumerate(rooms):
        print(f"  {i + 1}: {room.name}")
    print("  0: Return to Main Menu")
    
    while True:
        try:
            choice = int(input("Enter number: "))
            if choice == 0:
                return None
            if 1 <= choice <= len(rooms):
                return rooms[choice - 1]
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def select_device(room: Room) -> Optional[Device]:
    """Helper to select a device from a room."""
    devices = room.devices
    if not devices:
        print("There are no devices in this room.")
        return None
    
    print("\nSelect a device:")
    for i, device in enumerate(devices):
        # Use getattr to safely access 'name' attribute
        device_name = getattr(device, 'name', device.id)
        print(f"  {i + 1}: {device_name}")
    
    while True:
        try:
            choice = int(input("Enter number: "))
            if 1 <= choice <= len(devices):
                return devices[choice - 1]
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def manage_device(device: Device) -> None:
    """Menu to manage a single selected device."""
    device_name = getattr(device, 'name', device.id)
    while True:
        print(f"\n--- Managing: {device_name} ---")
        print(device)
        print("\nOptions:")
        print("  1: Turn On")
        print("  2: Turn Off")
        print("  3: Increase Intensity/Temperature")
        print("  4: Decrease Intensity/Temperature")
        if isinstance(device, SmartBulb):
            print("  5: Change Color")
        print("  0: Return to Previous Menu")

        choice = input("Enter your choice: ")
        try:
            if choice == '1':
                device.turn_on()
            elif choice == '2':
                device.turn_off()
            elif choice == '3':
                device.increase_intensity()
            elif choice == '4':
                device.decrease_intensity()
            elif choice == '5' and isinstance(device, SmartBulb):
                try:
                    r = int(input("Enter Red value (0-255): "))
                    g = int(input("Enter Green value (0-255): "))
                    b = int(input("Enter Blue value (0-255): "))
                    device.change_color(r, g, b)
                    print("Color changed successfully.")
                except ValueError as e:
                    print(f"Error: {e}")
            elif choice == '0':
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def manage_scheduler(scheduler: Scheduler) -> None:
    """Menu to manage a device's scheduler."""
    while True:
        print(scheduler)
        print("Scheduler Options:")
        print("  1: Add 'Turn On' Event")
        print("  2: Add 'Turn Off' Event")
        print("  3: Delete an Event")
        print("  0: Return to Main Menu")
        
        choice = input("Enter choice: ")
        if choice in ('1', '2'):
            action = 'turn_on' if choice == '1' else 'turn_off'
            try:
                day = input("Enter day (e.g., Monday): ")
                hour = int(input("Enter hour (0-23): "))
                minute = int(input("Enter minute (0-59): "))
                scheduler.add_event(day, hour, minute, 0, action)
                print("Event added successfully.")
            except (ValueError, InvalidTimeError) as e:
                print(f"Error: {e}")
        elif choice == '3':
            try:
                event_index = int(input("Enter the number of the event to delete: "))
                scheduler.delete_event(event_index - 1)
                print("Event deleted.")
            except (ValueError, IndexError) as e:
                print(f"Error: {e}")
        elif choice == '0':
            break
        else:
            print("Invalid choice.")

def manage_rooms(home: Home) -> None:
    """Menu to select and manage a room."""
    while True:
        room = select_room(home)
        if not room:
            break

        while True:
            print(f"\n--- Managing Room: {room.name} ---")
            print(room)
            print("\nRoom Options:")
            print("  1: Manage a Device")
            print("  2: Add a new Device")
            print("  3: Save Room History Log")
            print("  0: Return to Main Menu")

            choice = input("Enter your choice: ")
            if choice == '1':
                device = select_device(room)
                if device:
                    manage_device(device)
            elif choice == '2':
                add_new_device_to_room(home, room)
            elif choice == '3':
                room.save_log(LOG_FILE)
            elif choice == '0':
                return
            else:
                print("Invalid choice.")

def add_new_room(home: Home) -> None:
    """Handler to add a new room."""
    try:
        room_name = input("Enter the name for the new room: ")
        if room_name:
            home.add_room(room_name)
            print(f"Room '{room_name}' added successfully.")
        else:
            print("Room name cannot be empty.")
    except ValueError as e:
        print(f"Error: {e}")

def add_new_device_to_room(home: Home, room: Room) -> None:
    """Handler to add a new device to a specific room."""
    print("\nSelect device type:")
    print("  1: Smart Bulb")
    print("  2: Air Conditioner")
    dev_type = input("Enter type: ")

    name = input("Enter a name for the new device: ")
    if not name:
        print("Device name cannot be empty.")
        return

    try:
        device: Optional[Device] = None
        if dev_type == '1':
            is_prog = input("Is this bulb programmable? (y/n): ").lower() == 'y'
            device = SmartBulb(name=name, is_programmable=is_prog)
        elif dev_type == '2':
            device = AirConditioner(name=name)
        else:
            print("Invalid device type.")
            return
        
        home.add_device_to_room(device, room.name)
        print(f"Device '{name}' added to {room.name}.")

    except (ValueError, IndexError) as e:
        print(f"Invalid input: {e}")

def main_menu(home: Home) -> None:
    """Main interactive menu for the smart home."""
    while True:
        print("\n======= Smart Home Main Menu =======")
        print(home)
        print("\nOptions:")
        print("  1: Manage Rooms")
        print("  2: Add a new Room")
        print("  3: Manage Schedules")
        print("  9: Save and Exit")
        print("  0: Exit Without Saving")

        choice = input("Enter your choice: ")

        if choice == '1':
            if not home.rooms:
                print("No rooms exist. Please add a room first.")
                continue
            manage_rooms(home)
        elif choice == '2':
            add_new_room(home)
        elif choice == '3':
            programmable_devices = [dev for dev in home.get_all_devices() if dev.is_programmable]
            if not programmable_devices:
                print("No programmable devices found.")
                continue
            
            print("\nSelect a device for scheduling:")
            for i, dev in enumerate(programmable_devices):
                dev_name = getattr(dev, 'name', dev.id)
                print(f"  {i + 1}: {dev_name}")
            
            try:
                choice = int(input("Enter number: "))
                if 1 <= choice <= len(programmable_devices):
                    device = programmable_devices[choice - 1]
                    scheduler = home.get_scheduler_for_device(device.id)
                    if scheduler:
                        manage_scheduler(scheduler)
                    else:
                        print(f"Error: Could not find a scheduler for {device.id}.")
                else:
                    print("Invalid number.")
            except ValueError:
                print("Invalid input.")

        elif choice == '9':
            DataManager.save_home_to_json(home, DATA_FILE)
            print("Exiting.")
            break
        elif choice == '0':
            print("Exiting without saving.")
            break
        else:
            print("Invalid choice, please try again.")

def main() -> None:
    """Main function to load data and start the application."""
    print("--- Welcome to the Smart Home Management System (v2) ---")
    home = DataManager.load_home_from_json(DATA_FILE)
    
    if home is None:
        print("Starting with a new home setup.")
        home = Home(name="My First Smart Home")
        home.add_room("Living Room")
        home.add_device_to_room(SmartBulb(name="Living Room Lamp", is_programmable=True), "Living Room")
        home.add_device_to_room(AirConditioner(name="Main AC"), "Living Room")

    main_menu(home)

if __name__ == "__main__":
    main()
