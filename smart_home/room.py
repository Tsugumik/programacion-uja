import datetime
from typing import List, Dict, Any, Optional
from .device import Device
from .history_log import HistoryLog

class Room(HistoryLog):
    """Represents a room in the home, containing smart devices."""

    def __init__(self, name: str):
        """Initializes a Room."""
        if not name:
            raise ValueError("Room name cannot be empty.")
        self._name = name
        self._devices: Dict[str, Device] = {}

    @property
    def name(self) -> str:
        """Gets the room's name."""
        return self._name

    @property
    def devices(self) -> List[Device]:
        """Gets a list of devices in the room."""
        return list(self._devices.values())

    def add_device(self, device: Device) -> None:
        """Adds a device to the room."""
        if device.id in self._devices:
            raise ValueError(f"Device with ID '{device.id}' already exists in this room.")
        self._devices[device.id] = device

    def get_device_by_id(self, device_id: str) -> Optional[Device]:
        """Retrieves a device from the room by its ID."""
        return self._devices.get(device_id)

    def save_log(self, filename: str) -> None:
        """Appends the status of all devices in the room to a log file."""
        try:
            with open(filename, 'a') as f:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"--- Log for Room: {self.name} at {timestamp} ---\n")
                if not self._devices:
                    f.write("  (No devices in this room)\n")
                else:
                    for device in self._devices.values():
                        f.write(f"  - {device}\n")
                f.write("-" * (30 + len(self.name)) + "\n\n")
            print(f"Successfully saved log for room '{self.name}' to '{filename}'.")
        except IOError as e:
            print(f"Error saving log for room '{self.name}': {e}")

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the room to a dictionary."""
        return {
            "name": self.name,
            "devices": [device.to_dict() for device in self.devices]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], device_classes: Dict[str, type]) -> 'Room':
        """Creates a Room object from a dictionary."""
        room = cls(name=data["name"])
        for device_data in data.get("devices", []):
            device_type = device_data.get("type")
            device_class = device_classes.get(device_type)
            if device_class:
                device_obj = device_class.from_dict(device_data)
                room.add_device(device_obj)
            else:
                print(f"Warning: Unknown device type '{device_type}' found. Skipping.")
        return room

    def __str__(self) -> str:
        device_list = "\n".join(f"  - {dev.name} ({dev.id})" for dev in self.devices)
        if not device_list:
            device_list = "  (No devices in this room)"
        return f"[ Room: {self.name} ]\n{device_list}"
