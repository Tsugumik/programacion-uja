import json
import os
import itertools
from .home import Home
from .smart_bulb import SmartBulb
from .air_conditioner import AirConditioner

def save_home_to_json(home_object: Home, filename: str):
    """
    Serializes the Home object to a JSON file.
    Args:
        home_object: The Home instance to save.
        filename: The path to the output JSON file.
    """
    try:
        with open(filename, 'w') as f:
            json.dump(home_object.to_dict(), f, indent=4)
        print(f"Home state successfully saved to {filename}")
    except (IOError, TypeError) as e:
        print(f"Error saving home state: {e}")
        raise

def _synchronize_id_counters(home: Home):
    """
    Finds the highest ID for each device type in the loaded home
    and resets the class counters to the next available ID.
    """
    max_bulb_id = -1
    max_ac_id = -1

    for device in home.devices.values():
        dev_obj = device['object']
        try:
            id_num = int(dev_obj.id.split('_')[-1])
            if isinstance(dev_obj, SmartBulb):
                if id_num > max_bulb_id:
                    max_bulb_id = id_num
            elif isinstance(dev_obj, AirConditioner):
                if id_num > max_ac_id:
                    max_ac_id = id_num
        except (ValueError, IndexError):
            # Ignore devices with malformed IDs
            continue
    
    SmartBulb._id_counter = itertools.count(max_bulb_id + 1)
    AirConditioner._id_counter = itertools.count(max_ac_id + 1)
    print(f"ID counters synchronized. Next Bulb ID: {max_bulb_id + 1}, Next AC ID: {max_ac_id + 1}.")


def load_home_from_json(filename: str) -> Home | None:
    """
    Deserializes a Home object from a JSON file.
    Args:
        filename: The path to the input JSON file.
    Returns:
        A Home instance or None if the file doesn't exist.
    """
    if not os.path.exists(filename):
        return None

    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Use the class method to reconstruct the Home object
        home = Home.from_dict(data)
        
        # Synchronize the ID counters after loading all objects
        _synchronize_id_counters(home)
        
        print(f"Home state successfully loaded from {filename}")
        return home
    except (IOError, json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Error loading home state from {filename}: {e}")
        print("Starting with a new, empty home.")
        return Home() # Return a fresh instance on error
