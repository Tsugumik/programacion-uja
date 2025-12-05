import tkinter as tk
from tkinter import ttk
from smart_home.air_conditioner import AirConditioner
from .device_widget import DeviceWidget

class AirConditionerWidget(DeviceWidget):
    def __init__(self, parent, device: AirConditioner, controller):
        super().__init__(parent, device, controller)
        self.device: AirConditioner = device

        self._create_ac_widgets()
        self.update_widget()

    def _create_ac_widgets(self):
        # Temperature slider frame
        temp_frame = ttk.Frame(self)
        temp_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        temp_frame.columnconfigure(1, weight=1)

        temp_label = ttk.Label(temp_frame, text="Temperature")
        temp_label.grid(row=0, column=0, sticky="w")

        self.temp_var = tk.IntVar(value=self.device.temperature)
        self.temp_display_var = tk.StringVar()

        temp_slider = ttk.Scale(temp_frame, from_=16, to=30, orient=tk.HORIZONTAL, variable=self.temp_var, command=self.update_temperature)
        temp_slider.grid(row=0, column=1, sticky="ew", padx=5)
        
        temp_value_label = ttk.Label(temp_frame, textvariable=self.temp_display_var, width=4)
        temp_value_label.grid(row=0, column=2, sticky="e")


    def update_temperature(self, value):
        self.device.set_temperature(int(float(value)))
        self.update_widget()

    def update_widget(self):
        super().update_widget()
        self.temp_var.set(self.device.temperature)
        self.temp_display_var.set(f"{self.device.temperature}°C")
