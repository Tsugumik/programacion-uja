from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class Device(ABC):
    """Abstract base class for all smart devices."""

    def __init__(self, device_id: str, min_intensity: int, max_intensity: int):
        """Initializes a generic device."""
        self._id: str = device_id
        self._status: bool = False
        self._min_intensity: int = min_intensity
        self._max_intensity: int = max_intensity
        self._intensity: int = min_intensity

    @property
    def id(self) -> str:
        """The unique ID of the device."""
        return self._id

    @property
    def status(self) -> bool:
        """The status of the device (True for on, False for off)."""
        return self._status

    @property
    def intensity(self) -> int:
        """The current intensity of the device."""
        return self._intensity
        
    @property
    def is_programmable(self) -> bool:
        """Whether the device supports scheduling. Defaults to False."""
        return False

    def turn_on(self) -> None:
        """Turns the device on."""
        self._status = True

    def turn_off(self) -> None:
        """Turns the device off and resets intensity."""
        self._status = False
        self._intensity = self._min_intensity

    def set_intensity(self, value: int) -> None:
        """Sets the device's intensity to a specific value."""
        if self._min_intensity <= value <= self._max_intensity:
            self._intensity = value
        elif value < self._min_intensity:
            self._intensity = self._min_intensity
        else:
            self._intensity = self._max_intensity

    @abstractmethod
    def increase_intensity(self, amount: Optional[int] = None) -> None:
        """Increases the device's intensity."""
        pass

    @abstractmethod
    def decrease_intensity(self, amount: Optional[int] = None) -> None:
        """Decreases the device's intensity."""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the common device attributes to a dictionary."""
        return {
            "id": self.id,
            "status": self.status,
            "intensity": self.intensity,
            "type": self.__class__.__name__
        }

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Device':
        """Creates a device object from a dictionary."""
        pass

    def __str__(self) -> str:
        """Returns a string representation of the device."""
        status_str = "ON" if self.status else "OFF"
        return f"Device ID: {self.id}, Type: {self.__class__.__name__}, Status: {status_str}, Intensity: {self.intensity}"
