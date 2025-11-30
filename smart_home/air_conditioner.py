import itertools
from typing import Dict, Any, Optional
from .device import Device

class AirConditioner(Device):
    """
    Represents a smart air conditioner, a concrete implementation of a Device.
    Its intensity is managed as temperature.
    """
    _id_counter = itertools.count()
    DEFAULT_TEMP_INCREMENT = 1

    def __init__(self, name: str, initial_temp: int = 21):
        """
        Initializes an AirConditioner.

        Args:
            name: The name of the AC unit.
            initial_temp: The starting temperature. Defaults to 21°C.
        """
        super().__init__(device_id=f"AC_{next(AirConditioner._id_counter)}", min_intensity=16, max_intensity=30)
        self._name = name
        
        if self._min_intensity <= initial_temp <= self._max_intensity:
            self._intensity = initial_temp
        else:
            self._intensity = self._min_intensity

    @property
    def name(self) -> str:
        """Gets the name of the AC unit."""
        return self._name

    @property
    def temperature(self) -> int:
        """Gets the current target temperature (which is the intensity)."""
        return self.intensity

    def increase_intensity(self, amount: Optional[int] = None) -> None:
        """
        Increases the AC's target temperature.
        If amount is None or 0, it uses the default increment of 1.
        """
        increment = amount if amount else self.DEFAULT_TEMP_INCREMENT
        new_temp = self._intensity + increment
        if new_temp > self._max_intensity:
            self._intensity = self._max_intensity
            print(f"Temperature for {self.name} set to maximum ({self._max_intensity}°C).")
        else:
            self._intensity = new_temp

    def decrease_intensity(self, amount: Optional[int] = None) -> None:
        """
        Decreases the AC's target temperature.
        If amount is None or 0, it uses the default decrement of 1.
        """
        decrement = amount if amount else self.DEFAULT_TEMP_INCREMENT
        new_temp = self._intensity - decrement
        if new_temp < self._min_intensity:
            self._intensity = self._min_intensity
            print(f"Temperature for {self.name} set to minimum ({self._min_intensity}°C).")
        else:
            self._intensity = new_temp

    def __str__(self) -> str:
        status_str = "ON" if self.status else "OFF"
        return (f"Device: {self.name} ({self.id}) | Type: Air Conditioner | Status: {status_str} | "
                f"Temperature: {self.temperature}°C")

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the AC's state to a dictionary."""
        data = super().to_dict()
        data.update({
            "name": self.name
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AirConditioner':
        """Creates an AirConditioner instance from a dictionary."""
        ac = cls(name=data["name"])
        ac._id = data["id"]
        ac._status = data.get("status", False)
        # Use 'intensity' from dict for temperature
        ac._intensity = data.get("intensity", ac._min_intensity)
        return ac
