import time
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta


from time_tracker import Task, LogEntry, calc_elapsed_time
from google_sheets import Sheet
from utilities import Stopwatch


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
        self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=self.current_time)
        self.root.after(1000, self.update_clock)

    def update_timer(self):
        self.timer.set(self.sw.run_timer())
        self.root.after(1000, self.update_timer)

    def start_task(self):
        self.task = Task(self.new_task_entry.get())
        self.entry = LogEntry(self.task)
        self.entry.set_start_time()
        self.sw.start()
        self.update_timer()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_task(self):
        self.entry.set_stop_time()
        self.sw.stop()
        self.sw.reset()
        self.elapsed = calc_elapsed_time(self.entry.start, self.entry.stop)
        self.timer.set(self.elapsed)
        print(f"Time elapsed: {self.elapsed}")
        self.task.addTime(self.elapsed)
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        # Add log entry to sheet
        self.sheet.add_log_entry(self.entry)
        time.sleep(2)
        self.sheet.update_total_task_times()


def main():
    Gui(Sheet())


if __name__ == "__main__":
    main()
