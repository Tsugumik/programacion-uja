import itertools

class SmartBulb:
    """Represents a smart bulb."""
    _id_counter = itertools.count()

    def __init__(self, name="Bulb_1", is_programmable=False):
        self._id = f"Bulb_{next(self._id_counter)}"
        self._name = name
        self._is_on = False
        self._intensity = 0
        self._color = {'r': 255, 'g': 255, 'b': 255}
        self._is_programmable = is_programmable

    @property
    def id(self):
        """Gets the unique ID of the bulb."""
        return self._id

    @property
    def name(self):
        """Gets the name of the bulb."""
        return self._name

    @property
    def is_on(self):
        """Checks if the bulb is on."""
        return self._is_on

    @property
    def intensity(self):
        """Gets the intensity of the bulb."""
        return self._intensity

    @property
    def color(self):
        """Gets the color of the bulb."""
        return self._color

    @property
    def is_programmable(self):
        """Checks if the bulb is programmable."""
        return self._is_programmable

    def turn_on(self):
        """Turns the bulb on."""
        self._is_on = True
        if self._intensity == 0:
            self._intensity = 100

    def turn_off(self):
        """Turns the bulb off."""
        self._is_on = False
        self._intensity = 0

    def get_status(self):
        """Gets the current status of the bulb."""
        status = "ON" if self._is_on else "OFF"
        return f"Bulb '{self._name}': {status}, Intensity: {self._intensity}%, Color: RGB({self._color['r']}, {self._color['g']}, {self._color['b']})"

    def change_intensity(self, level):
        """
        Changes the intensity of the bulb.

        Args:
            level (int): The new intensity level.

        Raises:
            ValueError: If the intensity is not between 0 and 100.
        """
        if 0 <= level <= 100:
            self._intensity = level
        else:
            raise ValueError("Error: Intensity must be between 0 and 100")

    def change_color(self, r, g, b):
        """
        Changes the color of the bulb.

        Args:
            r (int): Red component (0-255).
            g (int): Green component (0-255).
            b (int): Blue component (0-255).

        Raises:
            ValueError: If the color values are not between 0 and 255.
        """
        if all(0 <= value <= 255 for value in [r, g, b]):
            self._color['r'] = r
            self._color['g'] = g
            self._color['b'] = b
        else:
            raise ValueError("Error: Color must be between 0 and 255")

    def __str__(self):
        header = "=" * 40
        status_str = 'ON' if self._is_on else 'OFF'
        return (f"{header}\n"
                f"BULB: {self._name}\n"
                f"Status: {status_str}\n"
                f"Intensity: {self._intensity}%\n"
                f"Color RGB: ({self._color['r']}, {self._color['g']}, {self._color['b']})\n"
                f"{header}")
