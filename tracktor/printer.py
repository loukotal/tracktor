from rich.console import Console
from rich.table import Table

from database import TracktorLog


class Printer:
    def __init__(self) -> None:
        self.console = Console()

    def print_stats(self):
        pass

    def print_logs(self):
        pass

    def print_log(self, time_log: TracktorLog):
        table = Table()
        log = time_log.to_dict()

        [table.add_column(col) for col in log.keys()]