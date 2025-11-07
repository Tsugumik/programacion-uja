import time

from smart_home.smart_bulb import SmartBulb

class InvalidTimeError(ValueError):
    """Custom exception for invalid time values."""
    pass

class Scheduler:
    """Schedules on/off events for a SmartBulb."""
    def __init__(self, smart_bulb: SmartBulb):
        if not isinstance(smart_bulb, SmartBulb):
            raise TypeError("Scheduler must be initialized with a SmartBulb object.")
        self._smart_bulb = smart_bulb
        self._schedule = []  # List of dictionaries: {'day': 'Monday', 'hour': 10, 'minute': 30, 'second': 0, 'action': 'turn_on'}

    @property
    def smart_bulb(self):
        """Gets the SmartBulb object associated with this scheduler."""
        return self._smart_bulb

    @property
    def schedule(self):
        """Gets the current schedule."""
        return self._schedule

    def get_week_days(self) -> list:
        """Returns a list of week days in English."""
        return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def get_system_time(self) -> str:
        """Returns the current system time in 'DayOfWeek-HH:MM:SS' format."""
        current_time = time.localtime()
        day_of_week = self.get_week_days()[current_time.tm_wday]
        return time.strftime(f"{day_of_week}-%H:%M:%S", current_time)

    def _validate_event_time(self, day: str, hour: int, minute: int, second: int):
        """Validates the day, hour, minute, and second for an event."""
        if day not in self.get_week_days():
            raise InvalidTimeError(f"Invalid day: {day}. Must be one of {self.get_week_days()}.")
        if not (0 <= hour <= 23):
            raise InvalidTimeError(f"Invalid hour: {hour}. Must be between 0 and 23.")
        if not (0 <= minute <= 59):
            raise InvalidTimeError(f"Invalid minute: {minute}. Must be between 0 and 59.")
        if not (0 <= second <= 59):
            raise InvalidTimeError(f"Invalid second: {second}. Must be between 0 and 59.")

    def add_start_event(self, day: str, hour: int, minute: int, second: int):
        """
        Adds a 'turn on' event to the schedule.

        Args:
            day (str): Day of the week (e.g., 'Monday').
            hour (int): Hour (0-23).
            minute (int): Minute (0-59).
            second (int): Second (0-59).

        Raises:
            InvalidTimeError: If any time component is invalid.
        """
        self._validate_event_time(day, hour, minute, second)
        event = {'day': day, 'hour': hour, 'minute': minute, 'second': second, 'action': 'turn_on'}
        self._schedule.append(event)
        self._schedule.sort(key=lambda x: (self.get_week_days().index(x['day']), x['hour'], x['minute'], x['second']))

    def add_end_event(self, day: str, hour: int, minute: int, second: int):
        """
        Adds a 'turn off' event to the schedule.

        Args:
            day (str): Day of the week (e.g., 'Monday').
            hour (int): Hour (0-23).
            minute (int): Minute (0-59).
            second (int): Second (0-59).

        Raises:
            InvalidTimeError: If any time component is invalid.
        """
        self._validate_event_time(day, hour, minute, second)
        event = {'day': day, 'hour': hour, 'minute': minute, 'second': second, 'action': 'turn_off'}
        self._schedule.append(event)
        self._schedule.sort(key=lambda x: (self.get_week_days().index(x['day']), x['hour'], x['minute'], x['second']))

    def delete_event(self, day: str, hour: int, minute: int, second: int, action: str):
        """
        Deletes a specific event from the schedule.

        Args:
            day (str): Day of the week.
            hour (int): Hour.
            minute (int): Minute.
            second (int): Second.
            action (str): 'turn_on' or 'turn_off'.

        Returns:
            bool: True if the event was deleted, False otherwise.

        Raises:
            InvalidTimeError: If any time component is invalid.
        """
        self._validate_event_time(day, hour, minute, second)
        event_to_delete = {'day': day, 'hour': hour, 'minute': minute, 'second': second, 'action': action}
        try:
            self._schedule.remove(event_to_delete)
            return True
        except ValueError:
            return False

    def check_and_execute_schedule(self):
        """
        Checks the current time against the schedule and executes events.
        This method would typically be called periodically by a main loop.
        """
        current_time = time.localtime()
        current_day = self.get_week_days()[current_time.tm_wday]
        current_hour = current_time.tm_hour
        current_minute = current_time.tm_min
        current_second = current_time.tm_sec

        for event in self._schedule:
            if (event['day'] == current_day and
                    event['hour'] == current_hour and
                    event['minute'] == current_minute and
                    event['second'] == current_second):
                if event['action'] == 'turn_on':
                    self._smart_bulb.turn_on()
                    print(f"[{self.get_system_time()}] Scheduled event: Turning on {self._smart_bulb.name}")
                elif event['action'] == 'turn_off':
                    self._smart_bulb.turn_off()
                    print(f"[{self.get_system_time()}] Scheduled event: Turning off {self._smart_bulb.name}")
                # Optionally, remove event after execution if it's a one-time event
                # self._schedule.remove(event)

    def __str__(self):
        header = "=" * 40
        schedule_str = "\n".join([f"  - {e['day']} {e['hour']:02d}:{e['minute']:02d}:{e['second']:02d} - {e['action'].replace('_', ' ').title()}"
                                 for e in self._schedule]) if self._schedule else "  No events scheduled."
        return (f"{header}\n"
                f"SCHEDULER for {self._smart_bulb.name}\n"
                f"Current System Time: {self.get_system_time()}\n"
                f"Schedule:\n{schedule_str}\n"
                f"{header}")
