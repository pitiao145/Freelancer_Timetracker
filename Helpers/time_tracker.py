import datetime

from time import localtime, strftime


# Time format
FMT = "%H:%M:%S"


# Classes


class Task:
    def __init__(self, name="Task", duration="00:00:00"):
        self.name = name
        self.duration = duration

    def __str__(self):
        return f"Task name: {self.name}\nTotal duration: {self.duration}"

    def addTime(self, t):
        current = datetime.datetime.strptime(self.duration, FMT)
        new = current + t

        self.duration = new.strftime(FMT)

    # Getter
    @property
    def name(self):
        return self._name

    # Setter for task name
    @name.setter
    def name(self, name: str):
        if not name.strip():
            raise ValueError("Fill in task description")
        self._name = name

    # Getter
    @property
    def duration(self):
        return self._duration

    # Setter for task duration
    @duration.setter
    def duration(self, duration: str):
        self._duration = duration


class LogEntry:
    def __init__(self, task: Task, start="00:00:00", stop="00:00:00"):
        self.date = datetime.date.today()
        self.task = task
        self.start = start
        self.stop = stop

    def __str__(self):
        return f"Date: {self.date}\nTask: {self.task.name}\nStart: {self.start}\nStop: {self.stop}"

    # Function used to set the start time of this log entry as the time at which this function is called.
    def set_start_time(self):
        self.start = strftime("%H:%M:%S", localtime())

    def set_stop_time(self):
        self.stop = strftime("%H:%M:%S", localtime())

    # Get the data to put in the activities log: date, activity name, start time and stop time
    def get_row_data(self):
        return [str(self.date), self.task.name, self.start, self.stop]

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if type(start) == str:
            self._start = start
        else:
            raise ValueError("Incorrect format")

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, stop):
        if type(stop) == str:
            self._stop = stop
        else:
            raise ValueError("Incorrect format")
