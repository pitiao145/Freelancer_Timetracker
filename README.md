# Freelancer time tracker

 ### Video Demo:
 ### Short Description: 
Time tracker that's able to record time spent on different tasks. It will save all the activities and their timestamps to a Google spreadsheet template. It also offers the possibility to get a list of the set of tasks performed on a day, and the total time spent on them. The program is implemented in an easy-to-use graphical user interface and allows for modifying the link of the spreadsheet to which the data should be written.
 ### Preview: 
<img width="354" alt="Screenshot 2023-09-14 at 08 47 56" src="https://github.com/pitiao145/Freelancer_Timetracker/assets/133644618/51d64c99-f469-4537-b7cd-1ce0d70337e2">



# Problem definition and scope of the project

This project was realized in the scope of CS50's introduction to programming with Python. For this final project, I wanted to think of a real-life problem I encountered in day-to-day life and try to solve this.

Pretty quickly, I realized that, on a daily basis, I was confronted with a problem when working as a freelancer. The current project I am working on as a front-end developer requires me to keep track of the hours I spend on the project in order to be able to bill the client at the end of the month. At the same time, I am required to fill in a KPI file for the client where I write down the specific tasks I worked on, and how many hours I spent on them. Since over the course of a day, I might be working on the same tasks, but at different times of the day, I used to write down my hours manually and then add up the total time I spent on each task, to then be able to fill in the KPI sheet.

Obviously, this problem can be solved by writing down times in a spreadsheet and extrapolating the data needed for the KPIs with the spreadsheet functionalities. I am also pretty sure there would already be existing apps to do just this, but I wanted to see if I was able to leverage the power of Python in order to develop something custom-made for my own needs and way of working. Also, when working as a freelancer, you need to put in place some systems to be able to track your time and the time you spend on different tasks. Developing this time-tracker will definitely save me some work and automate some parts of the process.

# Demo of the program

When the user uses the program for the first time, they will be prompted to fill in the link to a Google spreadsheet file, to which the program will write the log of activities. At this point, the program is based on a specific template, since it needs to know to which range of cells it needs to write the data. This could be customized for other templates in the future.

**Spreadsheet link prompt:**

<img width="206" alt="Screenshot 2023-09-14 at 09 00 01" src="https://github.com/pitiao145/Freelancer_Timetracker/assets/133644618/8e927183-4340-4b42-942b-60a8ee044df4">



**Empty template spreadsheet:**

<img width="1394" alt="Screenshot 2023-09-14 at 08 58 19" src="https://github.com/pitiao145/Freelancer_Timetracker/assets/133644618/6b60fa37-7181-4a5c-892e-ba14a9e67122">

This spreadsheet was made to make it easy for me to have a log of all the activities I did on a certain day (_activities log_ table on the above picture), as well as to have a daily recap of the activities I did with the total time spent on them (_tasks of the day_ table). The _Activities log_ table I can then send straight to the client in order to bill them for the work. The _Tasks of the day_ table I use to complete the KPI table from the client, I can just copy paste those values, which makes it really easy. Then, there is also a little table to show the total amount of hours worked and the pay I should expect for this. For this program to work optimally, the template should be prepopulated with 12 tabs, one for each month of the year. This is so that the program knows to which tab to write the data, in function of the date on which that the activities are recorded.


After the user fills in the link, the main GUI will load. If the user wants to change the spreadsheet link, they can always do so from the "edit" button in the main GUI. They will have to close the GUI in order to save this new link.

**Main GUI:**

<img width="353" alt="Screenshot 2023-09-14 at 09 00 24" src="https://github.com/pitiao145/Freelancer_Timetracker/assets/133644618/9584f20e-cebf-44ae-9f28-c89ab0b65b7c">


The user can then fill in a task, and press the start button. This will record the time at which this task was started. The user can then go on and perform their task while leaving the program running in the background. Once finished, pressing the stop button will record the stop time of the task, and the program will calculate the total elapsed time for this task. Then, these values will be sent to the spreadsheet by querying the Google Sheets API, and the sheet will be updated with the new activities log entry, and the "tasks of the day" tab will be updated as well to reflect the total task times.

**Sheet after a few activities**

<img width="1394" alt="Screenshot 2023-09-14 at 08 57 53" src="https://github.com/pitiao145/Freelancer_Timetracker/assets/133644618/41ebc0ac-820f-4a2c-bff8-d8b6f002beaa">


The user can also fill in a certain date for which they want to see the total task times, in case they forgot to fill in the KPI table on the same day as they performed the tasks (this is a useful feature for me as I often forget to fill in the KPI table on the same day).


# Code
## Structure of the project
The project is structured as follows:

<img width="176" alt="Screenshot 2023-09-14 at 09 27 19" src="https://github.com/pitiao145/Freelancer_Timetracker/assets/133644618/8109bb62-dce2-4950-a199-8d772cb81459">

*    `project.py` contains the main function. This file can be run with an optional `GUI` command line argument, which will then run the program with a GUI. If this file is run without a command line argument, the program can be entirely run from the terminal and has the same functionalities as described above.
Example usage: `python3 project.py <GUI>`
*    `test_project.py` contains the unit tests for the project.py file
*    The _Helpers_ folder contains some helping modules that were created for this program. We will go into these in the next section.
*    The _Config_ folder contains some configuration files related to authentication for the Google Sheets API


## project.py (main app)

Contains a `class Gui`, which has the whole GUI functionality. I decided to keep this class in the main python file in order to avoid circular imports since the GUI class uses some functions that are defined inside the _project.py_ file.

`main()` will check for the number of command line arguments. If none is given, it will run in the terminal. A while loop will prompt the user with different possible actions until the program is quit:
<img width="612" alt="Screenshot 2023-09-14 at 09 42 22" src="https://github.com/pitiao145/Freelancer_Timetracker/assets/133644618/217c4982-819f-433d-810f-c144f3fcf308">

If the `GUI` command line argument is given, then the program runs in a GUI built with the built-in _tkinter library_.

`def calc_elapsed_time(t_start, t_stop)`:
This function calculates the elapsed time between two points in time and returns the result as a _timedelta_ object.

`def create_entry(task)`:
This function takes a _Task_ object (class definition in the `time_tracker` file) as argument. A task object contains a task name and its total duration.
The function then creates a `LogEntry` object (class definition in the `time_tracker` file).

`def start_task(entry)`:
This will record the start time of the current LogEntry object.

`def stop_task(entry, sheet)`:
This will record the stop time of the current LogEntry object, calculate the elapsed time and add this to the total duration variable of the current Task object. It will then also call a function `update_total_task_times()` which will update all the data in the Google spreadsheet.


## Helpers

This folder contains all the helper files for this program.


### google_sheets

* `google_sheets.py` contains the Sheet class, which initializes the Google spreadsheet (with the URL the user provided). The ID for the file is saved in a JSON file in the Config folder.
* Every time this module is imported, there will be a check to see if there is a spreadsheet URL specified in the JSON file. If this is not the case, like on the first time the user uses this app for example, a separate GUI is started which will prompt the user for the spreadsheet ID, which will then be saved in the configuration file.
* the Sheet class contains a few class methods related to performing various spreadsheet operations, like writing the data of a _logEntry_ object to the spreadsheet and updating the total task times of a particular day. 
* This class is dependent on a few external libraries, which are all pip-installable. The libraries required can be found in the _requirements.txt_ file of this project.
  

### time_tracker

The time tracker module contains the class definition for the Task and logEntry objects.

A _Task_ object represents a single Task, and contains an attribute for the name and total duration of the task. The Task class also has a function that will calculate the total task time, and save that in the duration attribute of the Task object.

A _logEntry_ object contains a _Task_, a date and a start and  stop time for that _Task_ object. These objects are then used to populate the spreadsheet with the required information.

### utilities

This module contains a few classes and functions used in the _project.py_ file and other helper files.

* `Stopwatch` class is used to display the elapsed time in the GUI when a task has been started, so the user can always see the time they spent on a task.
* `start_setup_GUI` class is used to initialize the configuration GUI so the user can define the spreadsheet URL they want to use when first using the program.
* `def current_month()` is used to get the current month we are in, to define in which tab of the spreadsheet the data should be written.
* `get_sheet_id(url)`: this function uses a regex to check if the URL the user inputted is correct and if correct, it will return the actual spreadsheet ID from that URL, which is then used throughout the _google_sheets_ class.
* `def load_config()`: this function loads the configuration file from the Config folder
* `def save_config(config)`: saves the new configuration (i.e. the spreadsheet URL) when the user edits the URL in the GUI.
* `def save_link(new_link_value)` function used when the user updates the URL in the GUI. This uses the two previous functions to open and save the configuration file (config.json)
* `def get_current_link()`: gets the current link that is saved in the config.json file


### configuration files

This folder contains some configuration files to configure the _google_sheets_ class.
