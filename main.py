from smart_home.air_conditioner import AirConditioner
from smart_home.home import Home
from smart_home.scheduler import InvalidTimeError, Scheduler
from smart_home.smart_bulb import SmartBulb


def main():
    """Main function to demonstrate the smart home system."""
    print("=== Smart Home System Simulation ===\n")

    # 1. Create a Home
    my_home = Home()
    print("1. Home created.")

    # 2. Add rooms
    try:
        my_home.add_room("Living Room")
        my_home.add_room("Bedroom")
        my_home.add_room("Kitchen")
        print("2. Rooms added: ", my_home.rooms)
    except ValueError as e:
        print(f"Error adding room: {e}")

    # 3. Create devices
    bulb_living_room = SmartBulb(name="Living Room Bulb", is_programmable=True)
    bulb_kitchen = SmartBulb(name="Kitchen Bulb")
    ac_bedroom = AirConditioner(temperature=22.0)
    print("3. Devices created:")
    print(f"   - {bulb_living_room.id}: {bulb_living_room.name}")
    print(f"   - {bulb_kitchen.id}: {bulb_kitchen.name}")
    print(f"   - {ac_bedroom.id}")

    # 4. Add devices to the home
    try:
        my_home.add_device(bulb_living_room.id, bulb_living_room, "Living Room")
        my_home.add_device(bulb_kitchen.id, bulb_kitchen, "Kitchen")
        my_home.add_device(ac_bedroom.id, ac_bedroom, "Bedroom")
        print("\n4. Devices added to the home.")
        print(my_home)
    except ValueError as e:
        print(f"Error adding device: {e}")

    # 5. Interact with devices
    print("\n5. Interacting with devices...")
    try:
        living_room_bulb_obj = my_home.get_device_object(bulb_living_room.id)
        living_room_bulb_obj.turn_on()
        living_room_bulb_obj.change_intensity(80)
        living_room_bulb_obj.change_color(255, 200, 150)
        print(f"Living Room Bulb status: {living_room_bulb_obj.get_status()}")

        bedroom_ac_obj = my_home.get_device_object(ac_bedroom.id)
        bedroom_ac_obj.turn_on()
        bedroom_ac_obj.change_temperature(20)
        print(f"Bedroom AC status: {bedroom_ac_obj.get_status()}")
    except (ValueError, TypeError) as e:
        print(f"Error interacting with device: {e}")

    # 6. Demonstrate Scheduler
    print("\n6. Demonstrating the Scheduler...")
    if bulb_living_room.is_programmable:
        try:
            scheduler = Scheduler(bulb_living_room)
            print(f"Scheduler created for: {scheduler.smart_bulb.name}")

            # Add valid events
            print("   - Adding valid events...")
            scheduler.add_start_event("Monday", 18, 0, 0)
            scheduler.add_end_event("Monday", 23, 30, 0)
            print(scheduler)

            # Add an invalid event
            print("   - Trying to add an invalid event...")
            scheduler.add_start_event("InvalidDay", 10, 0, 0)

        except (TypeError, InvalidTimeError) as e:
            print(f"   - Caught expected error: {e}")

        try:
            # Try to create a scheduler for a non-bulb object
            print("\n   - Trying to create a scheduler for a non-bulb object...")
            invalid_scheduler = Scheduler(ac_bedroom)
        except TypeError as e:
            print(f"   - Caught expected error: {e}")
    else:
        print(f"The {bulb_living_room.name} is not programmable and cannot be scheduled.")

    # 7. Final Home Status
    print("\n7. Final Home Status:")
    print(my_home)

if __name__ == "__main__":
    main()
