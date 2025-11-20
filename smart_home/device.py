class Device:
    """Base class for all smart devices."""

    def __init__(self, min_intensity: int, max_intensity: int):
        """
        Initializes a generic device.
        The `_id` attribute is left empty and should be set by the subclass.

        Args:
            min_intensity: The minimum intensity level for the device.
            max_intensity: The maximum intensity level for the device.
        """
        self._id: str = ""
        self._status: bool = False
        self._min_intensity: int = min_intensity
        self._max_intensity: int = max_intensity
        self._intensity: int = min_intensity

    @property
    def id(self) -> str:
        """Gets the unique ID of the device."""
        return self._id

    @property
    def status(self) -> bool:
        """Gets the status of the device (True for on, False for off)."""
        return self._status

    @property
    def intensity(self) -> int:
        """Gets the current intensity of the device."""
        return self._intensity

    def turn_on(self) -> None:
        """Turns the device on."""
        self._status = True

    def turn_off(self) -> None:
        """Turns the device off and resets intensity to minimum."""
        self._status = False
        self._intensity = self._min_intensity

    def increase_intensity(self, amount: int = 1) -> None:
        """
        Increases the device's intensity.

        Args:
            amount: The amount to increase by.
        Raises:
            ValueError: If the new intensity exceeds the maximum limit.
        """
        new_intensity = self._intensity + amount
        if new_intensity > self._max_intensity:
            raise ValueError(f"Intensity cannot exceed maximum value of {self._max_intensity}.")
        self._intensity = new_intensity

    def decrease_intensity(self, amount: int = 1) -> None:
        """
        Decreases the device's intensity.

        Args:
            amount: The amount to decrease by.
        Raises:
            ValueError: If the new intensity goes below the minimum limit.
        """
        new_intensity = self._intensity - amount
        if new_intensity < self._min_intensity:
            raise ValueError(f"Intensity cannot go below minimum value of {self._min_intensity}.")
        self._intensity = new_intensity

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the device."""
        return {
            "id": self._id,
            "status": self._status,
            "intensity": self._intensity,
        }
