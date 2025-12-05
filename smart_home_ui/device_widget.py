import tkinter as tk
from tkinter import ttk
from smart_home.device import Device

class DeviceWidget(ttk.Frame):
    def __init__(self, parent, device: Device, controller):
        super().__init__(parent, padding="5")
        self.device = device
        self.controller = controller
        self.columnconfigure(1, weight=1)

        self._create_widgets()

    def _create_widgets(self):
        # Device name label
        name_label = ttk.Label(self, text=self.device.name)
        name_label.grid(row=0, column=0, sticky="w")

        # On/Off switch
        self.on_off_var = tk.BooleanVar(value=self.device.status)
        on_off_switch = ttk.Checkbutton(self, text="On/Off", variable=self.on_off_var, command=self.toggle_power)
        on_off_switch.grid(row=0, column=1, sticky="e")

    def toggle_power(self):
        if self.on_off_var.get():
            self.device.turn_on()
        else:
            self.device.turn_off()
        self.update_widget()

    def update_widget(self):
        self.on_off_var.set(self.device.status)
