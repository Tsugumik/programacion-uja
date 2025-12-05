import tkinter as tk
from tkinter import ttk
from smart_home.room import Room
from smart_home.smart_bulb import SmartBulb
from smart_home.air_conditioner import AirConditioner
from .smart_bulb_widget import SmartBulbWidget
from .air_conditioner_widget import AirConditionerWidget
from .device_widget import DeviceWidget
from .add_device_dialog import AddDeviceDialog

class RoomFrame(ttk.Frame):
    def __init__(self, parent, room: Room, controller):
        super().__init__(parent, padding="10", relief="groove", borderwidth=2)
        self.room = room
        self.controller = controller
        self.columnconfigure(0, weight=1)

        self._create_widgets()
        self.refresh_devices()

    def _create_widgets(self):
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header_frame.columnconfigure(0, weight=1)

        room_label = ttk.Label(header_frame, text=f"Room: {self.room.name}", font=("", 14, "bold"))
        room_label.grid(row=0, column=0, sticky="w")

        add_device_button = ttk.Button(header_frame, text="Add Device", command=self._open_add_device_dialog)
        add_device_button.grid(row=0, column=1, sticky="e", padx=(10, 0))

        self.devices_frame = ttk.Frame(self)
        self.devices_frame.grid(row=1, column=0, sticky="ew")
        self.devices_frame.columnconfigure(0, weight=1)

    def _open_add_device_dialog(self):
        AddDeviceDialog(self.master, self.controller, self.room)
        self.refresh_devices()

    def refresh_devices(self):
        for widget in self.devices_frame.winfo_children():
            widget.destroy()

        self.device_widgets = []
        if not self.room.devices:
            ttk.Label(self.devices_frame, text="No devices in this room.").pack(pady=10)
        else:
            for i, device in enumerate(self.room.devices):
                device_widget = self._create_device_widget(self.devices_frame, device)
                if device_widget:
                    device_widget.pack(fill=tk.X, pady=2)
                    self.device_widgets.append(device_widget)

    def _create_device_widget(self, parent, device):
        if isinstance(device, SmartBulb):
            return SmartBulbWidget(parent, device, self.controller)
        elif isinstance(device, AirConditioner):
            return AirConditionerWidget(parent, device, self.controller)
        else:
            return DeviceWidget(parent, device, self.controller)

    def update_frame(self):
        for widget in self.device_widgets:
            widget.update_widget()
