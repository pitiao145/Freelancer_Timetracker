import project
import datetime
from time_tracker import Task, LogEntry
from time import localtime, strftime, sleep
from google_sheets import Sheet



def test_calc_elapsed_time():
    assert project.calc_elapsed_time("09:00:00", "17:00:00") == datetime.timedelta(seconds=28800)

def test_create_entry():
    entry = project.create_entry("Test entry")
    assert entry.date == datetime.date.today()
    assert entry.task.name == "Test entry"
    assert entry.task.duration == "00:00:00"        


def test_start_task():
    entry = project.create_entry("Test entry")
    project.start_task(entry)
    assert entry.start == strftime("%H:%M:%S", localtime())


def test_stop_task():
    entry = project.create_entry("Test entry")
    sheet = Sheet()
    project.start_task(entry)
    sleep(3)
    assert project.stop_task(entry, sheet) == datetime.timedelta(seconds=3)

