from .smart_bulb import SmartBulb
from .air_conditioner import AirConditioner
from .scheduler import Scheduler

# A mapping from type names to class objects
DEVICE_CLASSES = {
    "SmartBulb": SmartBulb,
    "AirConditioner": AirConditioner,
}

class Home:
    """Represents a smart home with rooms, devices, and schedulers."""
    def __init__(self, name: str = "My Home"):
        self._name = name
        self._rooms = []
        self._devices = {}  # Maps device_id to {'object': device_obj, 'room': room_name}
        self._schedulers = {} # Maps device_id to Scheduler object

    @property
    def name(self) -> str:
        return self._name

    @property
    def rooms(self) -> list:
        """Gets the list of room names in the home."""
        return self._rooms.copy()

    @property
    def devices(self) -> dict:
        """Gets a copy of the devices dictionary."""
        return self._devices.copy()

    def add_room(self, room_name: str) -> None:
        """Adds a new room to the home."""
        if room_name in self._rooms:
            raise ValueError(f"Room '{room_name}' already exists.")
        self._rooms.append(room_name)

    def add_device_to_room(self, device_obj, room_name: str) -> None:
        """Adds a device object to a specified room."""
        if room_name not in self._rooms:
            raise ValueError(f"Room '{room_name}' does not exist.")
        if device_obj.id in self._devices:
            raise ValueError(f"Device with ID '{device_obj.id}' already exists.")
        self._devices[device_obj.id] = {'object': device_obj, 'room': room_name}
        if isinstance(device_obj, SmartBulb) and device_obj.is_programmable:
            self._schedulers[device_obj.id] = Scheduler(device_obj)

    def remove_device(self, device_id: str) -> None:
        """Removes a device from the home by its ID."""
        if device_id not in self._devices:
            raise ValueError(f"Device with ID '{device_id}' not found.")
        del self._devices[device_id]
        if device_id in self._schedulers:
            del self._schedulers[device_id]

    def get_device_by_id(self, device_id: str):
        """Retrieves a device object by its ID."""
        if device_id not in self._devices:
            raise ValueError(f"Device with ID '{device_id}' not found.")
        return self._devices[device_id]['object']
    
    def get_scheduler_for_device(self, device_id: str) -> Scheduler | None:
        """Retrieves the scheduler for a given device ID."""
        return self._schedulers.get(device_id)

    def get_devices_in_room(self, room_name: str) -> list:
        """Returns a list of device objects in a given room."""
        if room_name not in self._rooms:
            raise ValueError(f"Room '{room_name}' does not exist.")
        return [
            dev['object'] for dev in self._devices.values()
            if dev['room'] == room_name
        ]

    def __str__(self) -> str:
        report = [f"--- {self.name} Status ---"]
        if not self._rooms:
            report.append("This home has no rooms.")
        for room in self._rooms:
            report.append(f"\n[ Room: {room} ]")
            devices_in_room = self.get_devices_in_room(room)
            if not devices_in_room:
                report.append("  (No devices in this room)")
            else:
                for device in devices_in_room:
                    report.append(f"  - {device.name} ({device.id})")
        report.append("\n" + "-" * (len(self.name) + 18))
        return "\n".join(report)

    def to_dict(self) -> dict:
        """Serializes the Home object to a dictionary."""
        return {
            "name": self._name,
            "rooms": self._rooms,
            "devices": [
                {
                    "room": info["room"],
                    "device_data": info["object"].to_dict()
                }
                for info in self._devices.values()
            ],
            "schedulers": {dev_id: sched.to_dict() for dev_id, sched in self._schedulers.items()}
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Deserializes a Home object from a dictionary."""
        home = cls(name=data["name"])
        home._rooms = data.get("rooms", [])
        
        for device_entry in data.get("devices", []):
            device_data = device_entry["device_data"]
            device_type = device_data.get("type")
            
            device_class = DEVICE_CLASSES.get(device_type)
            if not device_class:
                print(f"Warning: Unknown device type '{device_type}' found in data. Skipping.")
                continue

            device_obj = device_class.from_dict(device_data)
            home.add_device_to_room(device_obj, device_entry["room"])
        
        # Load schedulers
        schedulers_data = data.get("schedulers", {})
        for dev_id, sched_data in schedulers_data.items():
            device = home.get_device_by_id(dev_id)
            if device:
                home._schedulers[dev_id] = Scheduler.from_dict(sched_data, device)

        return home
