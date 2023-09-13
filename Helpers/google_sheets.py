from __future__ import print_function

import os.path
import datetime
import Helpers.utilities as utilities

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet. Check if there is a google sheets link configured, otherwise start the setup GUI
if id_check := utilities.get_sheet_id(utilities.get_current_link()) == "":
    utilities.start_setup_GUI()
SPREADSHEET_ID = utilities.get_sheet_id(utilities.get_current_link())
CURRENT_MONTH = utilities.current_month()
# Range for the date column
RANGE_DATE = CURRENT_MONTH + "!A3:A100"
# Ranges for the activity log table
RANGE_FULL_LOG = CURRENT_MONTH + "!A3:F100"
RANGE_LOG_NAMES = CURRENT_MONTH + "!B3:B100"
RANGE_LOG_DURATION = CURRENT_MONTH + "!E3:E100"
# Ranges for the activities table
RANGE_ACTIVITIES = CURRENT_MONTH + "!G3:H100"
RANGE_ACTIVITIES_NAME = CURRENT_MONTH + "!G3:G100"
RANGE_ACTIVITIES_TOTAL_TIME = CURRENT_MONTH + "!H3:H100"


class Sheet:
    # Initialise the work log template on the current month's tab.
    def __init__(self, id=SPREADSHEET_ID):
        self.id = id
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("./Config/token.json"):
            self.creds = Credentials.from_authorized_user_file(
                "Config/token.json", SCOPES
            )
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                self.flow = InstalledAppFlow.from_client_secrets_file(
                    "./Config/credentials.json", SCOPES
                )
                self.creds = self.flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("./Config/token.json", "w") as self.token:
                self.token.write(self.creds.to_json())

        try:
            self.service = build("sheets", "v4", credentials=self.creds)

            # Call the Sheets API
            self.sheet = self.service.spreadsheets()
            print(f"Work sheet initialised. Current tab: {CURRENT_MONTH}")
        except HttpError as err:
            print(err)
        else:
            # Test if sheet id works, in case config.json has no value. Else the intialisation GUI will start
            sheet_test = (
                self.sheet.values().get(spreadsheetId=self.id, range="A1").execute()
            )

    # Adds an entry to the activity log. Enters today's date, the name of the task and the start and stop time of the task.
    def add_log_entry(self, logEntry):
        # Get the list of data to be written to the sheet
        values = logEntry.get_row_data()
        values.append(logEntry.task.duration)
        print(f"Values: {values}")
        # Write the data to the sheet
        body = {"values": [values]}

        result = (
            self.sheet.values()
            .append(
                spreadsheetId=self.id,
                range=RANGE_FULL_LOG,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )

        print("Log entry added")

    # This function returns a dictionary containing the set of the different tasks in the log, along with the total time spent on
    # each task. By default it get all the entries for today, but a specific date can also be passed in as an argument.
    def get_tasks_and_duration(self, date=str(datetime.date.today())):
        range_names = [RANGE_LOG_NAMES, RANGE_LOG_DURATION, RANGE_DATE]

        # First get all the tasks and their respective durations from the spreadsheet
        all_tasks = (
            self.sheet.values()
            .batchGet(spreadsheetId=self.id, ranges=range_names)
            .execute()
        )

        tasks = all_tasks.get("valueRanges")[0].get("values", [])
        durations = all_tasks.get("valueRanges")[1].get("values", [])
        dates = all_tasks.get("valueRanges")[2].get("values", [])

        # Put these values in a dictionary. Since one can work on the same tasks at different times during the day, we will need to
        # group the tasks by name and compute their total times in order to display this on the spreadsheet.
        tasks_dict = []
        for i in range(len(tasks)):
            try:
                tasks_dict.append(
                    {
                        "task_name": tasks[i][0],
                        "duration": durations[i][0],
                        "date": dates[i][0],
                    }
                )
            except IndexError:
                continue

        # Create a new dictionary to store the total duration for each task, for a certain date
        task_duration_totals = {}

        # Iterate through the list of dictionaries
        for task in tasks_dict:
            if task["date"] == date:
                name = task["task_name"]
                duration_str = task["duration"]

                # Parse the duration string into a datetime.timedelta object
                duration_parts = duration_str.split(":")
                hours = int(duration_parts[0])
                minutes = int(duration_parts[1])
                seconds = int(duration_parts[2])
                duration = datetime.timedelta(
                    hours=hours, minutes=minutes, seconds=seconds
                )

                # Check if the name is already in the dictionary
                if name in task_duration_totals:
                    # If it is, add the duration to the existing total
                    task_duration_totals[name] += duration
                else:
                    # If it's not, create a new entry in the dictionary
                    task_duration_totals[name] = duration
                # Convert the dictionary to a list of dictionaries with "name" and "duration" keys
                result = [
                    {"task_name": name, "duration": str(total)}
                    for name, total in task_duration_totals.items()
                ]
            else:
                continue

        try:
            return result
        except UnboundLocalError:
            print("There are no tasks yet today!")
            return [{"task_name": "No tasks for today yet!", "duration": "00:00:00"}]

    # Updates the total task times in the spreadsheet
    def update_total_task_times(self, date=str(datetime.date.today())):
        tasks = self.get_tasks_and_duration(date)

        # First clear the current cells before writing the new data.
        result = (
            self.sheet.values()
            .clear(
                spreadsheetId=self.id,
                range=RANGE_ACTIVITIES,
            )
            .execute()
        )

        nameValues = []
        for i in range(len(tasks)):
            nameValues.append([tasks[i]["task_name"]])

        timeValues = []
        for i in range(len(tasks)):
            timeValues.append([tasks[i]["duration"]])

        data = [
            {"range": RANGE_ACTIVITIES_NAME, "values": nameValues},
            {"range": RANGE_ACTIVITIES_TOTAL_TIME, "values": timeValues},
        ]

        body = {"valueInputOption": "USER_ENTERED", "data": data}

        result = (
            self.sheet.values().batchUpdate(spreadsheetId=self.id, body=body).execute()
        )

        print("Today's tasks updated")


def main():
    ...


if __name__ == "__main__":
    main()
