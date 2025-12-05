import tkinter as tk
from tkinter import ttk, messagebox
from smart_home.scheduler import InvalidTimeError

class ScheduleManagerDialog(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.transient(parent)
        self.title("Manage Schedules")
        self.controller = controller
        self.geometry("600x400")

        self.selected_device = tk.StringVar()
        self.devices = self.controller.get_programmable_devices()

        self._create_widgets()
        self.grab_set()
        self.wait_window(self)

    def _create_widgets(self):
        # Device selection
        device_frame = ttk.Frame(self)
        device_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(device_frame, text="Select Device:").pack(side=tk.LEFT)
        device_menu = ttk.OptionMenu(device_frame, self.selected_device, "Select a device", *[d.name for d in self.devices], command=self.on_device_select)
        device_menu.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Scheduler display
        self.schedule_display = tk.Listbox(self)
        self.schedule_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Add/Delete event buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(button_frame, text="Add 'Turn On' Event", command=lambda: self.add_event('turn_on')).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Add 'Turn Off' Event", command=lambda: self.add_event('turn_off')).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Delete Selected Event", command=self.delete_event).pack(side=tk.RIGHT)

    def on_device_select(self, device_name):
        self.refresh_schedule_display()

    def refresh_schedule_display(self):
        self.schedule_display.delete(0, tk.END)
        device = self._get_selected_device()
        if device:
            scheduler = self.controller.get_scheduler_for_device(device.id)
            if scheduler:
                for i, event in enumerate(scheduler.schedule):
                    self.schedule_display.insert(tk.END, f"{i+1}: {event['day']} {event['hour']:02d}:{event['minute']:02d} - {event['action']}")

    def _get_selected_device(self):
        selected_name = self.selected_device.get()
        for device in self.devices:
            if device.name == selected_name:
                return device
        return None

    def add_event(self, action):
        device = self._get_selected_device()
        if not device:
            messagebox.showerror("Error", "Please select a device first.")
            return

        # Simple dialog for event details
        dialog = AddEventDialog(self, action)
        if dialog.result:
            day, hour, minute = dialog.result
            try:
                scheduler = self.controller.get_scheduler_for_device(device.id)
                scheduler.add_event(day, hour, minute, 0, action)
                self.refresh_schedule_display()
            except (ValueError, InvalidTimeError) as e:
                messagebox.showerror("Error", str(e))

    def delete_event(self):
        device = self._get_selected_device()
        if not device:
            messagebox.showerror("Error", "Please select a device first.")
            return
        
        selected_indices = self.schedule_display.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select an event to delete.")
            return

        try:
            scheduler = self.controller.get_scheduler_for_device(device.id)
            scheduler.delete_event(selected_indices[0])
            self.refresh_schedule_display()
        except (ValueError, IndexError) as e:
            messagebox.showerror("Error", str(e))


class AddEventDialog(tk.Toplevel):
    def __init__(self, parent, action):
        super().__init__(parent)
        self.transient(parent)
        self.title(f"Add '{action}' Event")
        self.result = None

        self.day_var = tk.StringVar(value="Monday")
        self.hour_var = tk.IntVar(value=12)
        self.minute_var = tk.IntVar(value=0)

        self._create_widgets()
        self.grab_set()
        self.wait_window(self)

    def _create_widgets(self):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        ttk.Label(self, text="Day:").pack(padx=10, pady=2)
        ttk.OptionMenu(self, self.day_var, self.day_var.get(), *days).pack(padx=10, pady=2)
        
        ttk.Label(self, text="Hour (0-23):").pack(padx=10, pady=2)
        ttk.Spinbox(self, from_=0, to=23, textvariable=self.hour_var).pack(padx=10, pady=2)

        ttk.Label(self, text="Minute (0-59):").pack(padx=10, pady=2)
        ttk.Spinbox(self, from_=0, to=59, textvariable=self.minute_var).pack(padx=10, pady=2)

        ttk.Button(self, text="Add", command=self.add).pack(pady=10)

    def add(self):
        self.result = (self.day_var.get(), self.hour_var.get(), self.minute_var.get())
        self.destroy()
