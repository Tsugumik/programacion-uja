import itertools
from .device import Device

class AirConditioner(Device):
    """Represents a smart air conditioner, inheriting from Device."""
    _id_counter = itertools.count()

    def __init__(self, name: str, initial_temp: int = 21):
        super().__init__(min_intensity=16, max_intensity=30)
        self._id = f"AC_{next(AirConditioner._id_counter)}"
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
        """Gets the current temperature (which is the intensity)."""
        return self.intensity

    def __str__(self) -> str:
        status_str = "ON" if self.status else "OFF"
        return (f"Device: {self.name} ({self.id})\n"
                f"  Type: Air Conditioner\n"
                f"  Status: {status_str}\n"
                f"  Temperature: {self.temperature}°C")

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the AC's state."""
        data = super().to_dict()
        data.update({
            "type": "AirConditioner",
            "name": self._name
        })
        return data

    @classmethod
    def from_dict(cls, data: dict):
        """Creates an AirConditioner instance from a dictionary."""
        ac = cls(name=data["name"])
        ac._id = data["id"]
        ac._status = data["status"]
        ac._intensity = data["intensity"]
        return ac
