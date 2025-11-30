import time
from typing import List, Dict, Any
from .device import Device

class InvalidTimeError(ValueError):
    """Custom exception for invalid time values."""
    pass

class Scheduler:
    """Schedules on/off events for any programmable device."""

    def __init__(self, device: Device):
        """Initializes a Scheduler for a given Device."""
        if not isinstance(device, Device):
            raise TypeError("Scheduler must be initialized with a Device object.")
        if not device.is_programmable:
            raise ValueError("Device must be programmable to be scheduled.")
        self._device = device
        self._schedule: List[Dict[str, Any]] = []

    @property
    def device(self) -> Device:
        """Gets the Device object associated with this scheduler."""
        return self._device

    @property
    def schedule(self) -> List[Dict[str, Any]]:
        """Gets the current schedule."""
        return self._schedule

    @classmethod
    def get_week_days(cls) -> List[str]:
        """Returns a list of week days in English."""
        return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    @classmethod
    def get_system_time(cls) -> str:
        """Returns the current system time in 'DayOfWeek-HH:MM:SS' format."""
        current_time = time.localtime()
        day_of_week = cls.get_week_days()[current_time.tm_wday]
        return time.strftime(f"{day_of_week}-%H:%M:%S", current_time)

    @staticmethod
    def _validate_event_time(day: str, hour: int, minute: int, second: int):
        """Validates the day, hour, minute, and second for an event."""
        if day not in Scheduler.get_week_days():
            raise InvalidTimeError(f"Invalid day: {day}.")
        if not (0 <= hour <= 23):
            raise InvalidTimeError(f"Invalid hour: {hour}.")
        if not (0 <= minute <= 59):
            raise InvalidTimeError(f"Invalid minute: {minute}.")
        if not (0 <= second <= 59):
            raise InvalidTimeError(f"Invalid second: {second}.")

    def add_event(self, day: str, hour: int, minute: int, second: int, action: str):
        """Adds an event to the schedule."""
        self._validate_event_time(day, hour, minute, second)
        if action not in ['turn_on', 'turn_off']:
            raise ValueError("Action must be 'turn_on' or 'turn_off'.")
        event = {'day': day, 'hour': hour, 'minute': minute, 'second': second, 'action': action}
        self._schedule.append(event)
        self._schedule.sort(key=lambda x: (self.get_week_days().index(x['day']), x['hour'], x['minute'], x['second']))

    def delete_event(self, event_index: int):
        """Deletes an event from the schedule by its index."""
        if 0 <= event_index < len(self._schedule):
            del self._schedule[event_index]
        else:
            raise IndexError("Event index out of range.")

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the Scheduler to a dictionary."""
        return {"schedule": self._schedule}

    @classmethod
    def from_dict(cls, data: Dict[str, Any], device: Device) -> 'Scheduler':
        """Deserializes a Scheduler from a dictionary."""
        scheduler = cls(device)
        scheduler._schedule = data.get("schedule", [])
        return scheduler

    def __str__(self):
        header = "=" * 40
        # Accessing device.name which is available on SmartBulb and AirConditioner
        device_name = getattr(self._device, 'name', self._device.id)
        schedule_str = "\n".join([f"  {i+1}: {e['day']} {e['hour']:02d}:{e['minute']:02d}:{e['second']:02d} - {e['action'].replace('_', ' ').title()}"
                                 for i, e in enumerate(self._schedule)]) if self._schedule else "  No events scheduled."
        return (f"{header}\n"
                f"SCHEDULER for {device_name}\n"
                f"Current System Time: {self.get_system_time()}\n"
                f"Schedule:\n{schedule_str}\n"
                f"{header}")
