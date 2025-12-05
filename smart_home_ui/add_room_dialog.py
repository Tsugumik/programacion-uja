import tkinter as tk
from tkinter import ttk, messagebox

class AddRoomDialog(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.transient(parent)
        self.title("Add New Room")
        self.controller = controller
        self.result = None

        self.name_var = tk.StringVar()

        self._create_widgets()
        self.grab_set()
        self.wait_window(self)

    def _create_widgets(self):
        ttk.Label(self, text="Enter the name for the new room:").pack(padx=10, pady=5)
        
        name_entry = ttk.Entry(self, textvariable=self.name_var)
        name_entry.pack(padx=10, pady=5, fill=tk.X, expand=True)
        name_entry.focus_set()

        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=10)

        ttk.Button(button_frame, text="Add", command=self._add_room).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def _add_room(self):
        room_name = self.name_var.get().strip()
        if not room_name:
            messagebox.showerror("Error", "Room name cannot be empty.")
            return
        
        try:
            self.controller.add_room(room_name)
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
