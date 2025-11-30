import json
import os
import itertools
from typing import Optional

from .smart_bulb import SmartBulb
from .air_conditioner import AirConditioner
from .home import Home


class DataManager:
    """Utility class to save and load the home state from a JSON file."""

    @staticmethod
    def _synchronize_id_counters(home: 'Home') -> None:
        """Synchronizes ID counters after loading to prevent ID conflicts."""
        max_bulb_id = -1
        max_ac_id = -1

        for device in home.get_all_devices():
            try:
                id_num = int(device.id.split('_')[-1])
                if isinstance(device, SmartBulb):
                    if id_num > max_bulb_id:
                        max_bulb_id = id_num
                elif isinstance(device, AirConditioner):
                    if id_num > max_ac_id:
                        max_ac_id = id_num
            except (ValueError, IndexError):
                print(f"Warning: Could not parse ID '{device.id}'.")
                continue
        
        SmartBulb._id_counter = itertools.count(max_bulb_id + 1)
        AirConditioner._id_counter = itertools.count(max_ac_id + 1)
        print(f"ID counters synchronized. Next Bulb ID: {max_bulb_id + 1}, Next AC ID: {max_ac_id + 1}.")

    @staticmethod
    def save_home_to_json(home_object: 'Home', filename: str) -> None:
        """Serializes the Home object to a JSON file."""
        try:
            with open(filename, 'w') as f:
                json.dump(home_object.to_dict(), f, indent=4)
            print(f"Home state successfully saved to {filename}")
        except (IOError, TypeError) as e:
            print(f"Error saving home state: {e}")
            raise

    @staticmethod
    def load_home_from_json(filename: str) -> Optional['Home']:
        """Deserializes a Home object from a JSON file."""
        if not os.path.exists(filename):
            print("No data file found.")
            return None

        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            home = Home.from_dict(data)
            
            DataManager._synchronize_id_counters(home)
            
            print(f"Home state successfully loaded from {filename}")
            return home
        except (IOError, json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Error loading home state from '{filename}': {e}")
            print("Starting with a new, empty home due to loading error.")
            return Home("Recovery Home")
