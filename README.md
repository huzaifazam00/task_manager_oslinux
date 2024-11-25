Task Manager GUI for Linux
This project is a Task Manager GUI for Linux, built using Python, Tkinter for the graphical user interface (GUI), and psutil for system and process monitoring. It provides an interface to view, manage, and terminate running processes on the system, similar to the Task Manager found in Windows. Additionally, it tracks CPU and memory usage, and logs data for further analysis.

Features
View Running Processes: Display processes with PID, name, user, CPU, and memory usage.
System Performance: Real-time monitoring of CPU and memory usage.
Kill Processes: Select a process and terminate it using the "Kill Process" button.
Data Logging: Logs system performance and running tasks to a JSON file.
Automatic Updates: The task list and system performance data are updated every 5 seconds.

Requirements
Python 3.6+
psutil library for process and system monitoring.
Tkinter for the graphical user interface.
Linux-based OS (for process management).
Installation
Clone the repository:
bash
Copy code

"git clone https://github.com/yourusername/task-manager-gui.git"

cd task-manager-gui
Create and activate a virtual environment (optional but recommended):

bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install required dependencies:

bash
Copy code
pip install -r requirements.txt
Install psutil (if not in requirements.txt):

bash
Copy code
pip install psutil
Usage
Run the application:

bash
Copy code
python3 task_manager_gui.py
Grant Permissions:

If you encounter permission issues when killing a process, make sure to run the program with elevated privileges (using sudo):

bash
Copy code
sudo python3 task_manager_gui.py
Features:

View running processes in the table.
Check CPU and memory usage.
Select a process and click the Kill Process button to terminate it.
Data is saved to task_manager_data.json every 5 seconds.
Data Logging
The program logs the following data to task_manager_data.json every 5 seconds:

Timestamp
System performance metrics (CPU, memory)
Running tasks (PID, name, username, CPU, memory)
Current user
