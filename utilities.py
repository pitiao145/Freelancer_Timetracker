import datetime
import time

# Get the current month to know which sheet to access in the Google Spreadsheet
def current_month():
    today = datetime.date.today()
    month = today.strftime("%B")
    return month


# Class to be used in the GUI to display elapsed time
class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.running = False

    def start(self):
        if not self.running:
            self.start_time = time.time() - (
                self.start_time - time.time() if self.start_time else 0
            )
            self.running = True

    def stop(self):
        if self.running:
            self.start_time = time.time() - (
                self.start_time - time.time() if self.start_time else 0
            )
            self.running = False

    def reset(self):
        self.start_time = None
        self.running = False

    def elapsed_time(self):
        if self.start_time is None:
            return 0.0
        if self.running:
            return time.time() - self.start_time
        else:
            return self.start_time - time.time()

    def run_timer(self):
        elapsed = self.elapsed_time()
        hours, remainder = divmod(elapsed, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
