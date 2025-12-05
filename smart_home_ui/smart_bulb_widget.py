import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
from smart_home.smart_bulb import SmartBulb
from .device_widget import DeviceWidget

class SmartBulbWidget(DeviceWidget):
    def __init__(self, parent, device: SmartBulb, controller):
        super().__init__(parent, device, controller)
        self.device: SmartBulb = device

        self._create_bulb_widgets()
        self.update_widget() # Ensure color is set on creation

    def _create_bulb_widgets(self):
        # Add (P) to name if programmable
        if self.device.is_programmable:
            self.children['!label']['text'] = f"{self.device.name} (P)"

        # Intensity slider
        intensity_label = ttk.Label(self, text="Intensity")
        intensity_label.grid(row=1, column=0, sticky="w", padx=5)
        self.intensity_var = tk.IntVar(value=self.device.intensity)
        intensity_slider = ttk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.intensity_var, command=self.update_intensity)
        intensity_slider.grid(row=1, column=1, sticky="ew", padx=5)

        # Color chooser button and display
        color_frame = ttk.Frame(self)
        color_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
        color_frame.columnconfigure(1, weight=1)

        color_button = ttk.Button(color_frame, text="Change Color", command=self.change_color)
        color_button.grid(row=0, column=1, sticky="ew")

        self.color_display = tk.Frame(color_frame, width=20, height=20, relief="sunken", borderwidth=1)
        self.color_display.grid(row=0, column=0, padx=(0, 10), sticky="w")


    def update_intensity(self, value):
        self.device.set_intensity(int(float(value)))
        self.update_widget()

    def _get_color_hex(self) -> str:
        """Converts the device's RGB color to a hex string for Tkinter."""
        r, g, b = self.device.color['r'], self.device.color['g'], self.device.color['b']
        return f'#{r:02x}{g:02x}{b:02x}'

    def change_color(self):
        # askcolor returns a tuple ((r, g, b), '#rrggbb') or (None, None)
        color_tuple = askcolor(initialcolor=self._get_color_hex())
        if color_tuple and color_tuple[0] is not None:
            r, g, b = map(int, color_tuple[0])
            self.device.change_color(r, g, b)
            self.update_widget()

    def update_widget(self):
        super().update_widget()
        self.intensity_var.set(self.device.intensity)
        self.color_display.config(bg=self._get_color_hex())
