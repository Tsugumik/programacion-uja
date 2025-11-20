import itertools
from .device import Device

class SmartBulb(Device):
    """Represents a smart bulb, inheriting from Device."""
    _id_counter = itertools.count()

    def __init__(self, name: str, is_programmable: bool = False, color: str = "white"):
        super().__init__(min_intensity=0, max_intensity=100)
        self._id = f"Bulb_{next(SmartBulb._id_counter)}"
        self._name = name
        self._is_programmable = is_programmable
        self._color = color

    @property
    def name(self) -> str:
        """Gets the name of the bulb."""
        return self._name

    @property
    def is_programmable(self) -> bool:
        """Checks if the bulb is programmable."""
        return self._is_programmable

    @property
    def color(self) -> str:
        """Gets the current color of the bulb."""
        return self._color

    def set_color(self, new_color: str) -> None:
        """
        Sets the color of the bulb.

        Args:
            new_color: The new color string.
        Raises:
            ValueError: If the new_color string is empty or invalid.
        """
        if not new_color or not isinstance(new_color, str):
            raise ValueError("Color must be a non-empty string.")
        self._color = new_color

    def __str__(self) -> str:
        status_str = "ON" if self.status else "OFF"
        return (f"Device: {self.name} ({self.id})\n"
                f"  Type: Smart Bulb\n"
                f"  Status: {status_str}\n"
                f"  Intensity: {self.intensity}%\n"
                f"  Color: {self.color}")

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the bulb's state."""
        data = super().to_dict()
        data.update({
            "type": "SmartBulb",
            "name": self._name,
            "is_programmable": self._is_programmable,
            "color": self._color
        })
        return data

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a SmartBulb instance from a dictionary."""
        bulb = cls(name=data["name"], is_programmable=data["is_programmable"], color=data.get("color", "white"))
        bulb._id = data["id"]
        bulb._status = data["status"]
        bulb._intensity = data["intensity"]
        return bulb
