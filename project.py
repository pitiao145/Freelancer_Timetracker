import sys
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import time

import Helpers.google_sheets as gs
from Helpers.time_tracker import Task, LogEntry
import Helpers.utilities as utilities

# Time format
FMT = "%H:%M:%S"


# Define the graphical user interface for this app.
class Gui:
    def __init__(self, sheet):
        self.sheet = sheet
        self.root = tk.Tk()
        self.root.title("Task Time Tracker")
        self.root.geometry("350x300")  # Set the size to 450x300

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
        self.new_task_label.grid(row=1, column=0, padx=10)
        self.new_task_entry = ttk.Entry(self.root, width=15)
        self.new_task_entry.grid(row=1, column=1, padx=10, pady=5)

        # Start and Stop Buttons
        self.start_button = ttk.Button(
            self.root, text="Start", command=self.start_task, style="Green.TButton"
        )
        self.start_button.grid(row=2, column=0, padx=10, pady=5)
        self.stop_button = ttk.Button(
            self.root,
            text="Stop",
            command=self.stop_task,
            state=tk.DISABLED,
            style="Red.TButton",
        )
        self.stop_button.grid(row=2, column=1, padx=10, pady=5)

        # Total Time Label
        self.total_time_label = ttk.Label(
            self.root, text="Timer:", font=("Helvetica", 12)
        )
        self.total_time_label.grid(row=3, column=0, padx=10)
        # Initialize stopwatch and timer variable
        self.sw = utilities.Stopwatch()
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

        ##Configuration window
        # Configuration Section
        self.configuration_frame = ttk.Frame(self.root)
        self.configuration_frame.grid(row=0, column=1, pady=10, sticky="e")

        # Current google sheets link
        self.current_link = tk.StringVar()
        self.current_link.set(utilities.get_current_link())

        # Edit Button
        self.edit_button = ttk.Button(
            self.configuration_frame, text="Edit", command=self.open_editor, width=2.5
        )
        self.edit_button.grid(row=0, column=2, padx=2, pady=0)

        # Editor Window (separate Toplevel window)
        self.editor_window = None

        ## Update total task times field
        self.update_frame = ttk.Frame(self.root)
        self.update_frame.grid(row=6, columnspan=2, pady=10)
        # Update label
        self.update_label = ttk.Label(
            self.update_frame,
            text="Update the total task times for date:",
            font=("Helvetica", 12),
        )
        self.update_label.grid(row=0, column=0, padx=10, pady=10)
        # Update input
        self.update_input = ttk.Entry(self.update_frame, width=10)
        self.update_input.grid(row=0, column=1, padx=10, pady=10)
        # Update button
        self.update_button = ttk.Button(
            self.update_frame, text="Update", width=7, command=self.update_total_times
        )
        self.update_button.grid(row=1, columnspan=2, padx=10, pady=10)

        # Update the clock
        self.update_clock()

        # Mainloop
        self.root.mainloop()

    ## Class functions

    def update_clock(self):
        self.current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=self.current_time)
        self.root.after(1000, self.update_clock)

    def update_timer(self):
        self.timer.set(self.sw.run_timer())
        self.root.after(1000, self.update_timer)

    def start_task(self):
        try:
            self.entry = create_entry(self.new_task_entry.get())
        except ValueError:
            messagebox.showinfo(
                title="Message", message="Please input a valid task name."
            )
            return
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

    def open_editor(self):
        self.editor_window = tk.Toplevel(self.root)
        self.editor_window.title("Edit Google Sheets Link")

        # Display current Google Sheets link
        self.current_link_label = ttk.Label(
            self.editor_window, text="Current Google Sheets Link:"
        )
        self.current_link_label.grid(row=0, column=0, padx=10, sticky="w")

        self.link_display = ttk.Label(
            self.editor_window, textvariable=self.current_link, wraplength=400
        )
        self.link_display.grid(row=0, column=1, padx=10)

        # Input Field for Google Sheets Link
        self.link_entry = ttk.Entry(self.editor_window)
        self.link_entry.grid(row=1, columnspan=2, sticky="ew", pady=10)

        # Save Button
        self.save_button = ttk.Button(
            self.editor_window, text="Save", command=self.save_link
        )
        self.save_button.grid(row=2, column=1, sticky="w", padx=10, pady=10)

    # Validate and save the new link
    def save_link(self):
        self.new_link_value = self.link_entry.get()
        # Validate the new link here (e.g., regex)
        try:
            id = self.is_valid_link(self.new_link_value)
        except ValueError:
            # Display an error message to the user
            messagebox.showerror(
                title="Message", message="Google sheets link is not valid."
            )
            return
        else:
            self.current_link.set(self.new_link_value)
            # Update the configuration file with the new link
            utilities.save_link(self.new_link_value)
            # Close the editor window
            self.editor_window.destroy()

    # Function to check if the link is valid. Return the sheetId if valid.
    def is_valid_link(self, url):
        utilities.get_sheet_id(url)

    def update_total_times(self):
        date = self.update_input.get()
        if date == "":
            self.sheet.update_total_task_times()
        else:
            self.sheet.update_total_task_times(date)


def main():
    # Command line program
    if len(sys.argv) == 1:
        # Initialise the work sheet
        sheet = gs.Sheet()

        while True:
            option = input(
                "\nWhat do you want to do next?\n[1] Add new task\n[2] Start recording this task\n[3] Stop recording this task\n[4] See last task\n[5] See last log entry\n[6] Update sheet\n[7] Exit\n\n"
            )
            match option:
                case "1":
                    while True:
                        try:
                            entry = create_entry(input("Task name: "))
                        except ValueError:
                            print("Enter a valid name for the task.")
                            continue
                        else:
                            break
                case "2":
                    start_task(entry)
                case "3":
                    stop_task(entry, sheet)
                case "4":
                    print(entry.task)
                case "5":
                    print(entry)
                case "6":
                    date = input(
                        "For which day? Format YYYY-MM-DD (Leave blank if you want to update for today.)"
                    )
                    if date == "":
                        sheet.update_total_task_times()
                    else:
                        sheet.update_total_task_times(date)
                case "7":
                    try:
                        if entry.stop == "00:00:00":
                            ans = input(
                                "There's a task currently running, are you sure you want to exit? (Y/N)"
                            )
                            if ans == "No" or ans == "N" or ans == "n":
                                continue
                    except UnboundLocalError:
                        sys.exit()
                    else:
                        sys.exit()
                case _:
                    print("This is not an option")
                    continue
    # GUI program
    elif len(sys.argv) == 2 and sys.argv[1] == "GUI":
        # Initialise the work sheet
        sheet = gs.Sheet()
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


# Creates a log entry. Takes a new task's name as argument and returns an initialised entry object.
def create_entry(task):
    if task.strip().startswith("="):
        raise ValueError("Your task's name shouldn't start with '='.")
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
