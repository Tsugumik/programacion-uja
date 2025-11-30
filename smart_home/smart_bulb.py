import itertools
from typing import Dict, Any, Optional
from .device import Device

class SmartBulb(Device):
    """Represents a smart bulb, a concrete implementation of a Device."""
    _id_counter = itertools.count()
    DEFAULT_INTENSITY_INCREMENT = 10

    def __init__(self, name: str, is_programmable: bool = False, color: Optional[Dict[str, int]] = None):
        """Initializes a SmartBulb."""
        super().__init__(device_id=f"Bulb_{next(SmartBulb._id_counter)}", min_intensity=0, max_intensity=100)
        self._name = name
        self._is_programmable_flag = is_programmable
        
        if isinstance(color, dict) and all(k in color for k in ['r', 'g', 'b']):
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
        return self._is_programmable_flag

    @property
    def color(self) -> Dict[str, int]:
        """Gets the current RGB color of the bulb."""
        return self._color

    def increase_intensity(self, amount: Optional[int] = None) -> None:
        """Increases the bulb's intensity."""
        increment = amount if amount else self.DEFAULT_INTENSITY_INCREMENT
        new_intensity = self._intensity + increment
        if new_intensity > self._max_intensity:
            self._intensity = self._max_intensity
        else:
            self._intensity = new_intensity

    def decrease_intensity(self, amount: Optional[int] = None) -> None:
        """Decreases the bulb's intensity."""
        decrement = amount if amount else self.DEFAULT_INTENSITY_INCREMENT
        new_intensity = self._intensity - decrement
        if new_intensity < self._min_intensity:
            self._intensity = self._min_intensity
        else:
            self._intensity = new_intensity

    def change_color(self, r: int, g: int, b: int) -> None:
        """Changes the RGB color of the bulb."""
        if not all(0 <= val <= 255 for val in [r, g, b]):
            raise ValueError("Color values must be between 0 and 255.")
        self._color = {'r': r, 'g': g, 'b': b}

    def __str__(self) -> str:
        status_str = "ON" if self.status else "OFF"
        color_str = f"RGB({self._color.get('r', 0)}, {self._color.get('g', 0)}, {self._color.get('b', 0)})"
        return (f"Device: {self.name} ({self.id}) | Type: Smart Bulb | Status: {status_str} | "
                f"Intensity: {self.intensity}% | Color: {color_str}")

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the bulb's state to a dictionary."""
        data = super().to_dict()
        data.update({
            "name": self.name,
            "is_programmable": self.is_programmable,
            "color": self.color
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SmartBulb':
        """Creates a SmartBulb instance from a dictionary."""
        bulb = cls(
            name=data["name"],
            is_programmable=data.get("is_programmable", False),
            color=data.get("color")
        )
        bulb._id = data["id"]
        bulb._status = data.get("status", False)
        bulb._intensity = data.get("intensity", 0)
        return bulb
