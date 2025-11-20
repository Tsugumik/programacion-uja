import itertools
from .device import Device

class SmartBulb(Device):
    """Represents a smart bulb, inheriting from Device."""
    _id_counter = itertools.count()

    def __init__(self, name: str, is_programmable: bool = False, color: dict = None):
        super().__init__(min_intensity=0, max_intensity=100)
        self._id = f"Bulb_{next(SmartBulb._id_counter)}"
        self._name = name
        self._is_programmable = is_programmable
        
        # Defensive check for color data type to handle old/corrupted data
        if isinstance(color, dict):
            self._color = color
        else:
            self._color = {'r': 255, 'g': 255, 'b': 255}

    @property
    def name(self) -> str:
        """Gets the name of the bulb."""
        return self._name

    @property
    def is_programmable(self) -> bool:
        """Checks if the bulb is programmable."""
        return self._is_programmable

    @property
    def color(self) -> dict:
        """Gets the current RGB color of the bulb."""
        return self._color

    def change_color(self, r: int, g: int, b: int) -> None:
        """
        Changes the RGB color of the bulb.

        Args:
            r: Red component (0-255).
            g: Green component (0-255).
            b: Blue component (0-255).
        Raises:
            ValueError: If any color value is outside the 0-255 range.
        """
        if not all(0 <= val <= 255 for val in [r, g, b]):
            raise ValueError("Color values must be between 0 and 255.")
        self._color = {'r': r, 'g': g, 'b': b}

    def __str__(self) -> str:
        status_str = "ON" if self.status else "OFF"
        color_str = f"RGB({self._color.get('r', 0)}, {self._color.get('g', 0)}, {self._color.get('b', 0)})"
        return (f"Device: {self.name} ({self.id})\n"
                f"  Type: Smart Bulb\n"
                f"  Status: {status_str}\n"
                f"  Intensity: {self.intensity}%\n"
                f"  Color: {color_str}")

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
        bulb = cls(name=data["name"], is_programmable=data["is_programmable"], color=data.get("color"))
        bulb._id = data["id"]
        bulb._status = data["status"]
        bulb._intensity = data["intensity"]
        return bulb
