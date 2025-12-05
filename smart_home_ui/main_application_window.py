import tkinter as tk
from tkinter import ttk
import sv_ttk
from .room_frame import RoomFrame
from .add_room_dialog import AddRoomDialog
from .schedule_manager_dialog import ScheduleManagerDialog

class MainApplicationWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Smart Home Management System")
        self.geometry("1200x800")

        sv_ttk.set_theme("dark")

        self._create_widgets()
        self.refresh_rooms()

    def _create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(control_frame, text="Add New Room", command=self._open_add_room_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Manage Schedules", command=self._manage_schedules).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Save and Exit", command=self._save_and_exit).pack(side=tk.RIGHT, padx=5)
        ttk.Button(control_frame, text="Exit Without Saving", command=self._exit_without_saving).pack(side=tk.RIGHT, padx=5)

        self.canvas = tk.Canvas(main_frame)
        self.scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def refresh_rooms(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.room_frames = []
        rooms = self.controller.get_rooms()
        
        columns = 3
        for i in range(columns):
            self.scrollable_frame.columnconfigure(i, weight=1)

        for i, room in enumerate(rooms):
            row = i // columns
            col = i % columns
            
            room_frame = RoomFrame(self.scrollable_frame, room, self.controller)
            room_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.room_frames.append(room_frame)

    def _open_add_room_dialog(self):
        AddRoomDialog(self, self.controller)
        self.refresh_rooms()

    def _manage_schedules(self):
        ScheduleManagerDialog(self, self.controller)

    def _save_and_exit(self):
        self.controller.save_home()
        self.destroy()

    def _exit_without_saving(self):
        self.destroy()
