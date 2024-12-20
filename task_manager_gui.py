import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import os
import getpass
import json
from datetime import datetime

# Save data to a file
DATA_FILE = "task_manager_data.json"

def save_data_to_file(data):
    """Save task manager data to a JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def get_current_user():
    """Get the current logged-in user."""
    return getpass.getuser()

def get_system_performance():
    """Get system performance metrics."""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    return {
        "CPU Usage (%)": cpu_percent,
        "Memory Usage (%)": memory_percent,
        "Total Memory (GB)": round(memory.total / (1024**3), 2),
        "Available Memory (GB)": round(memory.available / (1024**3), 2),
    }

def get_running_tasks():
    """Get a list of running tasks."""
    tasks = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try:
            tasks.append(proc.info)
        except psutil.NoSuchProcess:
            pass
    return tasks

def update_gui():
    """Update the GUI with the latest task and system information."""
    tasks = get_running_tasks()
    for row in task_table.get_children():
        task_table.delete(row)

    for task in tasks:
        task_table.insert("", tk.END, values=(task['pid'], task['name'], task['username'], task['cpu_percent'], task['memory_percent']))

    performance = get_system_performance()
    cpu_label.config(text=f"CPU Usage: {performance['CPU Usage (%)']}%")
    memory_label.config(text=f"Memory Usage: {performance['Memory Usage (%)']}%")

    data_to_save = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "system_performance": performance,
        "running_tasks": tasks,
        "current_user": get_current_user()
    }
    save_data_to_file(data_to_save)

    root.after(5000, update_gui)  # Update every 5 seconds

def kill_process():
    """Kill the selected process."""
    selected_item = task_table.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a process to kill.")
        return

    try:
        pid = int(task_table.item(selected_item, "values")[0])  # Get PID from the selected row
        process = psutil.Process(pid)
        process.terminate()  # Attempt to terminate the process
        messagebox.showinfo("Process Killed", f"Process with PID {pid} has been terminated.")
        update_gui()  # Refresh the task list
    except psutil.NoSuchProcess:
        messagebox.showerror("Error", "The process no longer exists.")
    except psutil.AccessDenied:
        messagebox.showerror("Permission Denied", "You don't have permission to kill this process.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# GUI setup
root = tk.Tk()
root.title("Task Manager")
root.geometry("900x600")

# Current User
current_user_label = tk.Label(root, text=f"Current User: {get_current_user()}", font=("Arial", 12))
current_user_label.pack(pady=5)

# System Performance
performance_frame = tk.Frame(root)
performance_frame.pack(pady=10)

cpu_label = tk.Label(performance_frame, text="CPU Usage: ", font=("Arial", 12))
cpu_label.pack(side=tk.LEFT, padx=10)

memory_label = tk.Label(performance_frame, text="Memory Usage: ", font=("Arial", 12))
memory_label.pack(side=tk.LEFT, padx=10)

# Task Table
task_frame = tk.Frame(root)
task_frame.pack(pady=10)

columns = ("PID", "Name", "User", "CPU (%)", "Memory (%)")
task_table = ttk.Treeview(task_frame, columns=columns, show="headings", height=20)

for col in columns:
    task_table.heading(col, text=col)
    task_table.column(col, width=150)

task_table.pack()

# Kill Process Button
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

kill_button = tk.Button(button_frame, text="Kill Process", command=kill_process, bg="red", fg="white", font=("Arial", 12))
kill_button.pack()

# Start updating the GUI
update_gui()

# Run the GUI
root.mainloop()

