import datetime
import time
import json
import sys
import re
import tkinter as tk
from tkinter import ttk, messagebox


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


# Class to setup the google sheets links when first using the app.
class start_setup_GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Google sheets setup")
        self.root.geometry("300x300")

        # Input Field for Google Sheets Link
        self.link_entry = ttk.Entry(self.root)
        self.link_entry.grid(row=1, columnspan=2, sticky="ew", pady=10)

        # Save Button
        self.save_button = ttk.Button(self.root, text="Save", command=self.create_link)
        self.save_button.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        self.root.mainloop()

    def create_link(self):
        self.link_value = self.link_entry.get()
        # Update the configuration file with the new link
        try:
            save_link(self.link_value)
        except ValueError:
            messagebox.showerror(title="Fail", message="Link not valid")
        else:
            messagebox.showinfo(title="Success", message="Link saved")
        self.root.destroy()


# Get the current month to know which sheet to access in the Google Spreadsheet
def current_month():
    today = datetime.date.today()
    month = today.strftime("%B")
    return month


# Check a google sheet url for correctness, and return the sheet ID.
def get_sheet_id(url):
    if matches := re.search(
        r"^(?:https?://)?(?:www\.)?docs\.google\.com/spreadsheets/d/(\w+)(?:/.*)$",
        url.strip(),
    ):
        sheetId = matches.group(1)
        return sheetId
    elif url == "":
        return url
    else:
        raise ValueError


## Configuration functions
# Load the configuration file
def load_config():
    try:
        with open("./Config/config.json", "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        # Return a default configuration if the file doesn't exist
        sys.exit("Configuartion file doesn't exist")


# Save the updated configuration file
def save_config(config):
    with open("./Config/config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)


# Function to update the link in the configuration file
def save_link(new_link_value):
    # First check if the link is valid
    try:
        get_sheet_id(new_link_value)
    except:
        ValueError
        raise ValueError("Link is not valid")
    else:
        config = load_config()
        config["google_sheets_link"] = new_link_value
        save_config(config)


def get_current_link():
    config = load_config()
    link = config.get("google_sheets_link")
    return link


def main():
    ...


if __name__ == "__main__":
    main()
