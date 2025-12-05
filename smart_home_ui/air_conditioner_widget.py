import tkinter as tk
from tkinter import ttk
from smart_home.air_conditioner import AirConditioner
from .device_widget import DeviceWidget

class AirConditionerWidget(DeviceWidget):
    def __init__(self, parent, device: AirConditioner, controller):
        super().__init__(parent, device, controller)
        self.device: AirConditioner = device

        self._create_ac_widgets()

    def _create_ac_widgets(self):
        # Temperature slider
        temp_label = ttk.Label(self, text="Temperature")
        temp_label.grid(row=1, column=0, sticky="w")
        self.temp_var = tk.IntVar(value=self.device.temperature)
        temp_slider = ttk.Scale(self, from_=16, to=30, orient=tk.HORIZONTAL, variable=self.temp_var, command=self.update_temperature)
        temp_slider.grid(row=1, column=1, sticky="ew")

    def update_temperature(self, value):
        self.device.set_temperature(int(float(value)))
        self.update_widget()

    def update_widget(self):
        super().update_widget()
        self.temp_var.set(self.device.temperature)
