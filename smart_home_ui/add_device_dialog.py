import tkinter as tk
from tkinter import ttk, messagebox
from smart_home.room import Room
from smart_home.smart_bulb import SmartBulb
from smart_home.air_conditioner import AirConditioner

class AddDeviceDialog(tk.Toplevel):
    def __init__(self, parent, controller, room: Room):
        super().__init__(parent)
        self.transient(parent)
        self.title(f"Add Device to {room.name}")
        self.controller = controller
        self.room = room

        self.device_type_var = tk.StringVar()
        self.device_name_var = tk.StringVar()
        self.is_programmable_var = tk.BooleanVar()

        self._create_widgets()
        self.grab_set()
        self.wait_window(self)

    def _create_widgets(self):
        ttk.Label(self, text="Device Type:").pack(padx=10, pady=5)
        device_type_menu = ttk.OptionMenu(self, self.device_type_var, "Smart Bulb", "Smart Bulb", "Air Conditioner", command=self._on_device_type_change)
        device_type_menu.pack(padx=10, pady=5, fill=tk.X)

        ttk.Label(self, text="Device Name:").pack(padx=10, pady=5)
        name_entry = ttk.Entry(self, textvariable=self.device_name_var)
        name_entry.pack(padx=10, pady=5, fill=tk.X)
        name_entry.focus_set()

        self.programmable_check = ttk.Checkbutton(self, text="Programmable", variable=self.is_programmable_var)
        self.programmable_check.pack_forget()

        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=10)
        ttk.Button(button_frame, text="Add", command=self._add_device).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)
        
        self._on_device_type_change()

    def _on_device_type_change(self, *args):
        if self.device_type_var.get() == "Smart Bulb":
            self.programmable_check.pack(padx=10, pady=5, fill=tk.X)
        else:
            self.programmable_check.pack_forget()

    def _add_device(self):
        device_type = self.device_type_var.get()
        device_name = self.device_name_var.get().strip()

        if not device_name:
            messagebox.showerror("Error", "Device name cannot be empty.")
            return

        device = None
        if device_type == "Smart Bulb":
            device = SmartBulb(name=device_name, is_programmable=self.is_programmable_var.get())
        elif device_type == "Air Conditioner":
            device = AirConditioner(name=device_name)

        if device:
            try:
                self.controller.add_device_to_room(device, self.room.name)
                self.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Invalid device type selected.")
