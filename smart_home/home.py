from typing import List, Dict, Any, Iterator, Optional
from .room import Room
from .device import Device
from .smart_bulb import SmartBulb
from .air_conditioner import AirConditioner
from .scheduler import Scheduler

DEVICE_CLASSES = {
    "SmartBulb": SmartBulb,
    "AirConditioner": AirConditioner,
}

class Home:
    """Represents the entire smart home, aggregating rooms and schedulers."""

    def __init__(self, name: str = "My Home"):
        """Initializes the Home."""
        self._name = name
        self._rooms: Dict[str, Room] = {}
        self._schedulers: Dict[str, Scheduler] = {}  # Maps device_id to Scheduler

    @property
    def name(self) -> str:
        """Gets the name of the home."""
        return self._name

    @property
    def rooms(self) -> List[Room]:
        """Gets a list of all rooms in the home."""
        return list(self._rooms.values())

    def add_room(self, room_name: str) -> Room:
        """Adds a new room to the home."""
        if room_name in self._rooms:
            raise ValueError(f"Room '{room_name}' already exists.")
        room = Room(room_name)
        self._rooms[room_name] = room
        return room

    def get_room_by_name(self, room_name: str) -> Optional[Room]:
        """Retrieves a room by its name."""
        return self._rooms.get(room_name)

    def add_device_to_room(self, device: Device, room_name: str) -> None:
        """Adds a device to a specified room and creates a scheduler if applicable."""
        room = self.get_room_by_name(room_name)
        if not room:
            raise ValueError(f"Room '{room_name}' does not exist.")
        
        room.add_device(device)

        if device.is_programmable:
            self._schedulers[device.id] = Scheduler(device)

    def get_all_devices(self) -> Iterator[Device]:
        """Returns an iterator over all devices in all rooms."""
        for room in self._rooms.values():
            for device in room.devices:
                yield device

    def get_scheduler_for_device(self, device_id: str) -> Optional[Scheduler]:
        """Retrieves the scheduler for a given device ID."""
        return self._schedulers.get(device_id)

    def __str__(self) -> str:
        report = [f"--- {self.name} Status ---"]
        if not self._rooms:
            report.append("This home has no rooms.")
        else:
            for room in self._rooms.values():
                report.append(f"\n{room}")
        report.append("\n" + "-" * (len(self.name) + 18))
        return "\n".join(report)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the Home object to a dictionary."""
        return {
            "name": self.name,
            "rooms": [room.to_dict() for room in self.rooms],
            "schedulers": {dev_id: sched.to_dict() for dev_id, sched in self._schedulers.items()}
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Home':
        """Deserializes a Home object from a dictionary."""
        home = cls(name=data.get("name", "Unnamed Home"))
        
        for room_data in data.get("rooms", []):
            room = Room.from_dict(room_data, DEVICE_CLASSES)
            home._rooms[room.name] = room

        schedulers_data = data.get("schedulers", {})
        for dev_id, sched_data in schedulers_data.items():
            device = next((dev for dev in home.get_all_devices() if dev.id == dev_id), None)
            if device and device.is_programmable:
                home._schedulers[dev_id] = Scheduler.from_dict(sched_data, device)

        return home
