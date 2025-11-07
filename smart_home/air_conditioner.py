import itertools

class AirConditioner:
    """Represents a smart air conditioner."""
    _id_counter = itertools.count()

    def __init__(self, temperature=24.0):
        self._id = f"AC_{next(self._id_counter)}"
        self._temperature = temperature
        self._is_on = False

    @property
    def id(self):
        """Gets the unique ID of the air conditioner."""
        return self._id

    @property
    def temperature(self):
        """Gets the current temperature of the air conditioner."""
        return self._temperature

    @property
    def is_on(self):
        """Checks if the air conditioner is on."""
        return self._is_on

    def turn_on(self):
        """Turns the air conditioner on."""
        self._is_on = True

    def turn_off(self):
        """Turns the air conditioner off."""
        self._is_on = False

    def get_status(self):
        """Gets the current status of the air conditioner."""
        status = "ON" if self._is_on else "OFF"
        return f"Air conditioner is {status}, Temperature: {self._temperature}°C"

    def change_temperature(self, new_temperature):
        """
        Changes the temperature of the air conditioner.

        Args:
            new_temperature (float): The new temperature.

        Raises:
            ValueError: If the temperature is not between 16 and 30 degrees Celsius.
        """
        if 16 <= new_temperature <= 30:
            self._temperature = new_temperature
        else:
            raise ValueError("Error: Temperature must be between 16 and 30 degrees Celsius.")

    def __str__(self):
        header = "=" * 40
        status_str = 'ON' if self._is_on else 'OFF'
        return (f"{header}\n"
                f"CLIMATIZER\n"
                f"Status: {status_str}\n"
                f"Temperature: {self._temperature}°C\n"
                f"{header}")
