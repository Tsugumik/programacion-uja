from typing import Protocol

class HistoryLog(Protocol):
    """An interface for objects that can save a historical log."""
    
    def save_log(self, filename: str) -> None:
        """Appends the current state to a log file."""
        ...
