import sys
import datetime

from google_sheets import Sheet
from GUI import Gui
import time
from time_tracker import Task, LogEntry, calc_elapsed_time


def main():
    # Initialise the work sheet
    sheet = Sheet()
    GUI = Gui(sheet)
    # while True:
    #     option = input(
    #         "\nWhat do you want to do next?\n[1] Add new task\n[2] Start recording this task\n[3] Stop recording this task\n[4] See task\n[5] Update sheet\n[6] See log entry\n[7] Exit\n"
    #     )

    #     match option:
    #         case "1":
    #             task = Task(input("Task name: "))
    #         case "2":
    #             entry = LogEntry(task)
    #             entry.set_start_time()
    #         case "3":
    #             entry.set_stop_time()
    #             elapsed = calc_elapsed_time(entry.start, entry.stop)
    #             print(f"Time elapsed: {elapsed}")
    #             task.addTime(elapsed)

    #             # Add log entry to sheet
    #             sheet.add_log_entry(entry)
    #             time.sleep(2)
    #             sheet.update_total_task_times()
    #         case "4":
    #             print(task)
    #         case "5":
    #             sheet.update_total_task_times()
    #         case "6":
    #             print(entry)
    #         case "7":
    #             sys.exit()
    #         case _:
    #             print("This is not an option")
    #             continue


if __name__ == "__main__":
    main()
