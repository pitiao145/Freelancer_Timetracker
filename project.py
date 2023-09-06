import sys
import datetime
import tkinter as tk
from tkinter import ttk

from google_sheets import Sheet
import time
from time_tracker import Task, LogEntry
from utilities import Stopwatch

# Time format
FMT = "%H:%M:%S"

class Gui:
    def __init__(self, sheet):
        self.sheet = sheet
        self.root = tk.Tk()
        self.root.title("Task Time Tracker")
        self.root.geometry("300x200")  # Set the size to 200x200

        # Configure grid columns and rows to expand
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(4, weight=1)

        # Title Label
        self.title_label = ttk.Label(
            self.root, text="Task Time Tracker", font=("Helvetica", 16)
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # New Task Input Field
        self.new_task_label = ttk.Label(
            self.root, text="New task:", font=("Helvetica", 12)
        )
        self.new_task_label.grid(row=1, column=0, sticky="w", padx=10)
        self.new_task_entry = ttk.Entry(self.root, width=20)
        self.new_task_entry.grid(row=1, column=1, padx=10, pady=5)

        # Start and Stop Buttons
        self.start_button = ttk.Button(
            self.root, text="Start", command=self.start_task, style="Green.TButton"
        )
        self.start_button.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.stop_button = ttk.Button(
            self.root,
            text="Stop",
            command=self.stop_task,
            state=tk.DISABLED,
            style="Red.TButton",
        )
        self.stop_button.grid(row=2, column=1, padx=10, pady=5, sticky="e")

        # Total Time Label
        self.total_time_label = ttk.Label(
            self.root, text="Timer:", font=("Helvetica", 12)
        )
        self.total_time_label.grid(row=3, column=0, padx=10)
        # Initialize stopwatch and timer variable
        self.sw = Stopwatch()
        self.timer = tk.StringVar()
        self.timer.set("00:00:00")
        self.total_time_display = ttk.Label(
            self.root, textvariable=self.timer, font=("Helvetica", 12)
        )
        self.total_time_display.grid(row=3, column=1, padx=10)

        # Clock Label
        self.clock_label = ttk.Label(self.root, text="", font=("Helvetica", 12))
        self.clock_label.grid(row=4, column=0, columnspan=2, pady=(20, 10))

        # Configure button styles
        self.style = ttk.Style()
        self.style.configure(
            "Green.TButton", foreground="green", font=("Helvetica", 12)
        )
        self.style.configure("Red.TButton", foreground="red", font=("Helvetica", 12))

        # Update the clock
        self.update_clock()

        self.root.mainloop()

    def update_clock(self):
        self.current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=self.current_time)
        self.root.after(1000, self.update_clock)

    def update_timer(self):
        self.timer.set(self.sw.run_timer())
        self.root.after(1000, self.update_timer)

    def start_task(self):
        self.task = Task(self.new_task_entry.get())
        self.entry = LogEntry(self.task)
        start_task(self.entry)
        self.sw.start()
        self.update_timer()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_task(self):
        self.elapsed = stop_task(self.entry, self.sheet)
        self.sw.stop()
        self.sw.reset()
        self.timer.set(self.elapsed)
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

       
def main():
    if len(sys.argv) == 1:
        # Initialise the work sheet
        sheet = Sheet()

        while True:
            option = input(
                "\nWhat do you want to do next?\n[1] Add new task\n[2] Start recording this task\n[3] Stop recording this task\n[4] See last task\n[5] See last log entry\n[6] Update sheet\n[7] Exit\n\n"
            )
            match option:
                case "1":
                    entry = create_entry(input("Task name: "))
                case "2":
                    start_task(entry)
                case "3":
                    stop_task(entry, sheet)
                case "4":
                    print(entry.task)
                case "5":
                    print(entry)
                case "6":
                    sheet.update_total_task_times()
                case "7":
                    sys.exit()
                case _:
                    print("This is not an option")
                    continue
    elif len(sys.argv) == 2 and sys.argv[1] == "GUI":
        # Initialise the work sheet
        sheet = Sheet()
        # Start the GUI
        interface = Gui(sheet)
    else:
        sys.exit("\nUsage: project.py <GUI>\n")


# Calculate the time-difference between two points in time, and return the result as a timedelta.
def calc_elapsed_time(t_start, t_stop):
    tdelta = datetime.datetime.strptime(t_stop, FMT) - datetime.datetime.strptime(
        t_start, FMT
    )
    return tdelta


def create_entry(task):
    task = Task(task)
    entry = LogEntry(task)
    print("\nTask created.\n")
    return entry


def start_task(entry):
    entry.set_start_time()
    print("\nTask started.\n")


def stop_task(entry, sheet):
    # Stop the counter and save the stop time
    entry.set_stop_time()
    elapsed = calc_elapsed_time(entry.start, entry.stop)
    # Calculate elapsed time and save it to the task
    print(f"\nTime elapsed: {elapsed}")
    entry.task.addTime(elapsed)
    # Add log entry to sheet
    sheet.add_log_entry(entry)
    time.sleep(2)
    sheet.update_total_task_times()

    return elapsed


if __name__ == "__main__":
    main()
