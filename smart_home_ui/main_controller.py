from smart_home.home import Home
from smart_home.device import Device
from smart_home.data_manager import DataManager
from .main_application_window import MainApplicationWindow

class MainController:
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.home = DataManager.load_home_from_json(self.data_file)
        if self.home is None:
            self.home = Home(name="My First Smart Home")
        
        self.view = MainApplicationWindow(self)

    def run(self):
        self.view.mainloop()

    def get_rooms(self):
        return self.home.rooms

    def add_room(self, room_name: str):
        self.home.add_room(room_name)

    def add_device_to_room(self, device: Device, room_name: str):
        self.home.add_device_to_room(device, room_name)

    def get_programmable_devices(self):
        return [dev for dev in self.home.get_all_devices() if dev.is_programmable]

    def get_scheduler_for_device(self, device_id: str):
        return self.home.get_scheduler_for_device(device_id)

    def save_home(self):
        DataManager.save_home_to_json(self.home, self.data_file)
