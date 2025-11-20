from smart_home.home import Home
from smart_home.smart_bulb import SmartBulb
from smart_home.air_conditioner import AirConditioner
from smart_home.persistence import load_home_from_json, save_home_to_json
from smart_home.scheduler import InvalidTimeError

DATA_FILE = "home_data.json"

def select_device(home, filter_fn=None):
    """Helper function to select a device from a list, with an optional filter."""
    all_devices = list(home.devices.values())
    devices_to_show = [dev['object'] for dev in all_devices if filter_fn is None or filter_fn(dev['object'])]

    if not devices_to_show:
        print("There are no devices matching the criteria.")
        return None
    
    print("\nSelect a device:")
    for i, device in enumerate(devices_to_show):
        print(f"  {i + 1}: {device.name} ({device.id})")
    
    while True:
        try:
            choice = int(input("Enter device number: "))
            if 1 <= choice <= len(devices_to_show):
                return devices_to_show[choice - 1]
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def manage_device(device) -> None:
    """Menu to manage a single selected device."""
    while True:
        print(f"\n--- Managing: {device.name} ---")
        print(device)
        print("\nOptions:")
        print("  1: Turn On")
        print("  2: Turn Off")
        print("  3: Increase Intensity/Temperature")
        print("  4: Decrease Intensity/Temperature")
        if isinstance(device, SmartBulb):
            print("  5: Change Color")
        print("  0: Return to Main Menu")

        choice = input("Enter your choice: ")
        try:
            if choice == '1':
                device.turn_on()
                print(f"{device.name} turned on.")
            elif choice == '2':
                device.turn_off()
                print(f"{device.name} turned off.")
            elif choice == '3':
                device.increase_intensity()
                print("Intensity/Temperature increased.")
            elif choice == '4':
                device.decrease_intensity()
                print("Intensity/Temperature decreased.")
            elif choice == '5' and isinstance(device, SmartBulb):
                try:
                    r = int(input("Enter Red value (0-255): "))
                    g = int(input("Enter Green value (0-255): "))
                    b = int(input("Enter Blue value (0-255): "))
                    device.change_color(r, g, b)
                    print(f"Color changed successfully.")
                except (ValueError) as e:
                    print(f"Error changing color: {e}. Please enter numbers between 0 and 255.")
            elif choice == '0':
                break
            else:
                print("Invalid choice, please try again.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def manage_scheduler(scheduler) -> None:
    """Menu to manage a scheduler for a device."""
    while True:
        print(scheduler)
        print("Scheduler Options:")
        print("  1: Add 'Turn On' Event")
        print("  2: Add 'Turn Off' Event")
        print("  3: Delete an Event")
        print("  0: Return to Main Menu")
        
        choice = input("Enter choice: ")
        if choice == '1' or choice == '2':
            action = 'turn_on' if choice == '1' else 'turn_off'
            try:
                day = input("Enter day (e.g., Monday): ")
                hour = int(input("Enter hour (0-23): "))
                minute = int(input("Enter minute (0-59): "))
                scheduler.add_event(day, hour, minute, 0, action)
                print("Event added successfully.")
            except (ValueError, InvalidTimeError) as e:
                print(f"Error adding event: {e}")
        elif choice == '3':
            try:
                event_index = int(input("Enter the number of the event to delete: "))
                scheduler.delete_event(event_index - 1)
                print("Event deleted.")
            except (ValueError, IndexError) as e:
                print(f"Error deleting event: {e}")
        elif choice == '0':
            break
        else:
            print("Invalid choice.")

def main_menu(home) -> None:
    """Main interactive menu for the smart home."""
    while True:
        print("\n======= Smart Home Main Menu =======")
        print(home)
        print("\nOptions:")
        print("  1: Manage a Device")
        print("  2: Manage Schedules")
        print("  3: Add a new Device")
        print("  4: Add a new Room")
        print("  9: Save and Exit")
        print("  0: Exit Without Saving")

        choice = input("Enter your choice: ")

        if choice == '1':
            device = select_device(home)
            if device:
                manage_device(device)
        elif choice == '2':
            programmable_bulb_filter = lambda d: isinstance(d, SmartBulb) and d.is_programmable
            bulb = select_device(home, filter_fn=programmable_bulb_filter)
            if bulb:
                scheduler = home.get_scheduler_for_device(bulb.id)
                if scheduler:
                    manage_scheduler(scheduler)
                else:
                    print(f"Error: Could not find a scheduler for {bulb.name}.")
        elif choice == '3':
            add_new_device(home)
        elif choice == '4':
            add_new_room(home)
        elif choice == '9':
            save_home_to_json(home, DATA_FILE)
            print("Exiting.")
            break
        elif choice == '0':
            print("Exiting without saving.")
            break
        else:
            print("Invalid choice, please try again.")

def add_new_room(home) -> None:
    """Handler to add a new room."""
    try:
        room_name = input("Enter the name for the new room: ")
        if not room_name:
            print("Room name cannot be empty.")
            return
        home.add_room(room_name)
        print(f"Room '{room_name}' added successfully.")
    except ValueError as e:
        print(f"Error: {e}")

def add_new_device(home) -> None:
    """Handler to add a new device."""
    if not home.rooms:
        print("You must add a room before adding a device.")
        return

    print("\nSelect device type:")
    print("  1: Smart Bulb")
    print("  2: Air Conditioner")
    dev_type = input("Enter type: ")

    name = input("Enter a name for the new device: ")
    if not name:
        print("Device name cannot be empty.")
        return

    print("Select a room:")
    for i, room in enumerate(home.rooms):
        print(f"  {i + 1}: {room}")
    
    try:
        room_choice = int(input("Enter room number: "))
        if not (1 <= room_choice <= len(home.rooms)):
            print("Invalid room number.")
            return
        room_name = home.rooms[room_choice - 1]

        if dev_type == '1':
            is_prog = input("Is this bulb programmable? (y/n): ").lower() == 'y'
            device = SmartBulb(name=name, is_programmable=is_prog)
        elif dev_type == '2':
            device = AirConditioner(name=name)
        else:
            print("Invalid device type.")
            return
        
        home.add_device_to_room(device, room_name)
        print(f"Device '{name}' added to {room_name}.")

    except (ValueError, IndexError) as e:
        print(f"Invalid input: {e}")


def main() -> None:
    """Main function to load data and start the application."""
    print("--- Welcome to the Smart Home Management System ---")
    home = load_home_from_json(DATA_FILE)
    
    if home is None:
        print("No saved data found. Starting with a new home.")
        home = Home(name="My First Home")
        # Optional: Create a default setup
        home.add_room("Living Room")
        home.add_device_to_room(SmartBulb(name="Living Room Lamp", is_programmable=True), "Living Room")
        home.add_device_to_room(AirConditioner(name="Main AC"), "Living Room")

    main_menu(home)

if __name__ == "__main__":
    main()
