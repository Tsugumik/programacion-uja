class Home:
    """Represents a smart home with rooms and devices."""
    def __init__(self):
        self._rooms = []
        self._devices = {}

    @property
    def rooms(self):
        """Gets the list of rooms in the home."""
        return self._rooms

    @property
    def devices(self):
        """Gets the dictionary of devices in the home."""
        return self._devices

    def add_room(self, room_name):
        """
        Adds a new room to the home.

        Args:
            room_name (str): The name of the room to add.

        Raises:
            ValueError: If the room already exists.
        """
        if room_name in self._rooms:
            raise ValueError(f"The room '{room_name}' already exists.")
        self._rooms.append(room_name)

    def add_device(self, device_id, device_object, room):
        """
        Adds a device to a specified room in the home.

        Args:
            device_id (str): The unique ID of the device.
            device_object: The device object (e.g., SmartBulb, AirConditioner).
            room (str): The room where the device is located.

        Raises:
            ValueError: If the room does not exist or the device ID already exists.
        """
        if room not in self._rooms:
            raise ValueError(f"Room '{room}' does not exist.")
        if device_id in self._devices:
            raise ValueError(f"Device ID '{device_id}' already exists.")
        self._devices[device_id] = {
            'object': device_object,
            'room': room
        }

    def remove_device(self, device_id):
        """
        Removes a device from the home.

        Args:
            device_id (str): The ID of the device to remove.

        Raises:
            ValueError: If the device does not exist.
        """
        if device_id not in self._devices:
            raise ValueError(f"Device '{device_id}' does not exist.")
        del self._devices[device_id]

    def get_device_location(self, device_id):
        """
        Gets the location (room) of a device.

        Args:
            device_id (str): The ID of the device.

        Returns:
            str: The name of the room where the device is located.

        Raises:
            ValueError: If the device does not exist.
        """
        if device_id not in self._devices:
            raise ValueError(f"Device '{device_id}' not found.")
        return self._devices[device_id]['room']

    def get_device_object(self, device_id):
        """
        Gets the device object by its ID.

        Args:
            device_id (str): The ID of the device.

        Returns:
            object: The device object.

        Raises:
            ValueError: If the device does not exist.
        """
        if device_id not in self._devices:
            raise ValueError(f"Device '{device_id}' not found.")
        return self._devices[device_id]['object']

    def count_devices(self):
        """
        Counts the total number of devices in the home.

        Returns:
            int: The total number of devices.
        """
        return len(self._devices)

    def count_devices_by_room(self, room_name):
        """
        Counts the number of devices in a specific room.

        Args:
            room_name (str): The name of the room.

        Returns:
            int: The number of devices in the room.
        """
        count = 0
        for device_info in self._devices.values():
            if device_info['room'] == room_name:
                count += 1
        return count

    def get_devices_in_room(self, room_name):
        """
        Gets a list of device IDs in a specific room.

        Args:
            room_name (str): The name of the room.

        Returns:
            list: A list of device IDs in the specified room.
        """
        devices_in_room = []
        for device_id, device_info in self._devices.items():
            if device_info['room'] == room_name:
                devices_in_room.append(device_id)
        return devices_in_room

    def __str__(self):
        header = "=" * 40
        rooms_str = ", ".join(self._rooms) if self._rooms else "No rooms"
        devices_str = "\n".join([f"  - {dev_id} ({info['object'].__class__.__name__}) in {info['room']}"
                                 for dev_id, info in self._devices.items()]) if self._devices else "  No devices"

        return (f"{header}\n"
                f"SMART HOME STATUS\n"
                f"Rooms: {rooms_str}\n"
                f"Devices:\n{devices_str}\n"
                f"{header}")
