import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
import time
import threading
import pygame

# Initialize the pygame mixer
pygame.mixer.init()

def play_notification():
    """Play a single notification sound."""
    global notification_sound
    notification_sound = pygame.mixer.Sound('notification.wav')
    notification_sound.play()

def play_alarm():
    """Play an alarm sound continuously."""
    global alarm_sound
    alarm_sound = pygame.mixer.Sound('alarm.wav')
    alarm_sound.play(loops=-1)  # Play continuously

def stop_all_sounds():
    """Stop all currently running sounds."""
    pygame.mixer.stop()

# Function to monitor the file for changes
def monitor_file(file_path, text_area, log_area, stop_event):
    last_content = ""

    # Check if the file is initially empty
    with open(file_path, 'r') as file:
        file_content = file.read()
        file_was_empty = len(file_content.strip()) == 0  # Check if the file is empty (ignores whitespace)

    while not stop_event.is_set():
        try:
            with open(file_path, 'r') as file:
                current_content = file.read()

                if current_content != last_content:
                    text_area.delete(1.0, tk.END)
                    text_area.insert(tk.END, current_content)
                    text_area.yview(tk.END)

                    if file_was_empty and current_content.strip():
                        play_alarm()
                        file_was_empty = False  # Update to indicate the file is no longer empty
                        log_area.insert(tk.END, "File was initially empty. Alarm sound played.\n")
                    else:
                        play_notification()
                        log_area.insert(tk.END, f"Change detected at {time.strftime('%Y-%m-%d %H:%M:%S')}:\n")
                        if len(last_content) == 0:
                            log_area.insert(tk.END, "Initial content loaded:\n")
                        else:
                            log_area.insert(tk.END, "File content updated:\n")

                        # Log the difference between old and new content
                        last_lines = last_content.splitlines()
                        current_lines = current_content.splitlines()

                        for i, line in enumerate(current_lines):
                            if i >= len(last_lines) or line != last_lines[i]:
                                log_area.insert(tk.END, f"New line {i+1}: {line}\n")

                        for i in range(len(current_lines), len(last_lines)):
                            log_area.insert(tk.END, f"Line {i+1} removed.\n")

                        log_area.insert(tk.END, "\n")
                        log_area.yview(tk.END)

                    last_content = current_content

            time.sleep(1)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while monitoring the file: {str(e)}")
            stop_event.set()


# Function to start monitoring
def start_monitoring():
    file_path = file_entry.get()
    if not file_path:
        messagebox.showwarning("Warning", "Please select a file to monitor.")
        return

    stop_monitoring()  # Ensure any previous monitoring is stopped
    stop_event.clear()

    # Start a new thread to monitor the file
    monitoring_thread = threading.Thread(target=monitor_file, args=(file_path, text_area, log_area, stop_event))
    monitoring_thread.daemon = True
    monitoring_thread.start()
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    stop_notification_button.config(state=tk.NORMAL)

    # Log the start of monitoring
    log_area.insert(tk.END, f"Started monitoring file: {file_path}\n")
    log_area.insert(tk.END, f"Monitoring started at {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    log_area.yview(tk.END)

# Function to stop monitoring
def stop_monitoring():
    stop_event.set()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    stop_notification_button.config(state=tk.DISABLED)

    # Stop any playing sound
    stop_all_sounds()

    # Log the stop of monitoring
    log_area.insert(tk.END, f"Stopped monitoring at {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    log_area.yview(tk.END)

# Function to open file dialog and select a file
def select_file():
    file_path = filedialog.askopenfilename(title="Select Hashcat Output File")
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

# Create the main window with a modern look
window = tk.Tk()
window.title("Hashcat Output Monitor")
window.geometry("850x400")  # Set the initial size of the window

# Apply a theme
style = ttk.Style()
style.theme_use('clam')  # 'clam', 'alt', 'default', 'classic' are some options
style.configure('TFrame', background='#2E2E2E')
style.configure('TLabel', background='#2E2E2E', foreground='white', font=('Helvetica', 11))
style.configure('TButton', background='#1C86EE', foreground='white', font=('Helvetica', 10, 'bold'))
style.configure('TNotebook', background='#2E2E2E')
style.configure('TNotebook.Tab', background='#3B3B3B', foreground='white', padding=[10, 5])

# Create tabs
tab_control = ttk.Notebook(window)
tab_monitor = ttk.Frame(tab_control, style='TFrame')
tab_logs = ttk.Frame(tab_control, style='TFrame')
tab_control.add(tab_monitor, text="Monitor")
tab_control.add(tab_logs, text="Logs")
tab_control.pack(expand=1, fill="both")

# Monitor tab layout with frames
frame_monitor = ttk.Frame(tab_monitor, padding="10", style='TFrame')
frame_monitor.pack(fill="both", expand=True)

label_file = ttk.Label(frame_monitor, text="Hashcat Output File:", style='TLabel')
label_file.grid(row=0, column=0, padx=10, pady=5, sticky='W')
file_entry = ttk.Entry(frame_monitor, width=60)
file_entry.grid(row=0, column=1, padx=10, pady=5, sticky='W')
browse_button = ttk.Button(frame_monitor, text="Browse", command=select_file, style='TButton')
browse_button.grid(row=0, column=2, padx=10, pady=5)

start_button = ttk.Button(frame_monitor, text="Start Monitoring", command=start_monitoring, style='TButton')
start_button.grid(row=1, column=0, padx=10, pady=10, sticky='W')
stop_button = ttk.Button(frame_monitor, text="Stop Monitoring", command=stop_monitoring, state=tk.DISABLED, style='TButton')
stop_button.grid(row=1, column=1, padx=10, pady=10, sticky='W')
stop_notification_button = ttk.Button(frame_monitor, text="Stop Notification", command=stop_all_sounds, state=tk.DISABLED, style='TButton')
stop_notification_button.grid(row=1, column=2, padx=10, pady=10, sticky='W')

text_area = scrolledtext.ScrolledText(frame_monitor, width=85, height=15, wrap=tk.WORD, background='#1C1C1C', foreground='white', font=('Helvetica', 10))
text_area.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Logs tab layout
frame_logs = ttk.Frame(tab_logs, padding="10", style='TFrame')
frame_logs.pack(fill="both", expand=True)

log_area = scrolledtext.ScrolledText(frame_logs, width=85, height=15, wrap=tk.WORD, background='#1C1C1C', foreground='white', font=('Helvetica', 10))
log_area.pack(fill="both", expand=True, padx=10, pady=10)

# Stop event for controlling the monitoring thread
stop_event = threading.Event()

# Run the application
window.mainloop()
