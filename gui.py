import tkinter as tk
from tkinter import messagebox, filedialog, Scrollbar, ttk
from activity_tracker import ActivityTracker
from data_upload import UploadManager
from config import Config
import threading
import time
import signal
import sys


config = Config()
tracker = ActivityTracker(config, log_file="activity_log.txt")
upload_manager = UploadManager()
tracking_thread = None
tracking_active = False


def start_tracking():
    global tracking_active, tracking_thread
    tracking_active = True
    tracking_thread = threading.Thread(target=tracking_loop)
    tracking_thread.start()
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    update_status("Status: Tracking Started", "green")


def stop_tracking():
    global tracking_active
    tracking_active = False
    if tracker:
        tracker.stop_listeners()
    update_status("Status: Tracking Stopped", "red")
    stop_button.config(state=tk.DISABLED)
    start_button.config(state=tk.NORMAL)


def update_status(text, color):
    status_label.config(text=text, foreground=color)

# The main tracking loop
def tracking_loop():
    while tracking_active:
        try:
            
            screenshot_path = tracker.capture_screenshot()

            
            activity_summary = tracker.get_activity_summary()
            formatted_summary = format_activity_summary(activity_summary)
            log_text.insert(tk.END, f"{formatted_summary}\n")
            log_text.yview(tk.END)  

            
            upload_manager.upload_to_dropbox(screenshot_path)

           
            time.sleep(config.screenshot_interval)
        except Exception as e:
            log_text.insert(tk.END, f"An error occurred: {e}\n")
            log_text.yview(tk.END)  
    log_text.insert(tk.END, "Tracking stopped.\n")
    log_text.yview(tk.END) 

# Function to format activity summary
def format_activity_summary(summary):
    current_mouse_clicks = summary.get('current_mouse_clicks', 0)
    previous_mouse_clicks = summary.get('previous_mouse_clicks', 0)
    current_keyboard_presses = summary.get('current_keyboard_presses', 0)
    previous_keyboard_presses = summary.get('previous_keyboard_presses', 0)
    
    mouse_text = (
        f"Current Mouse Clicks: {current_mouse_clicks}\n"
        f"Previous Mouse Clicks: {previous_mouse_clicks}\n"
    )
    keyboard_text = (
        f"Current Keyboard Presses: {current_keyboard_presses}\n"
        f"Previous Keyboard Presses: {previous_keyboard_presses}\n"
    )
    
    formatted_text = (
        f"=====================\n"
        f"Activity Summary:\n"
        f"=====================\n"
        f"{mouse_text}"
        f"{keyboard_text}"
        f"=====================\n"
    )
    
    return formatted_text


def manual_upload():
    file_path = filedialog.askopenfilename()
    if file_path:
        upload_manager.upload_to_dropbox(file_path)


def handle_shutdown(signum, frame):
    global tracking_thread
    stop_tracking()
    if tracking_thread and tracking_thread.is_alive():
        tracking_thread.join()
    upload_manager.retry_uploads()
    root.quit()  
    sys.exit(0)

signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)


def update_config():
    try:
        config.screenshot_interval = int(interval_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the screenshot interval.")
        return
    config.blur_screenshots = blur_var.get()
    tracker.config = config
    messagebox.showinfo("Settings Updated", "Configuration settings have been updated.")

# Hover effect functions
def on_enter(event):
    widget = event.widget
    widget.config(background="#3e8e41", foreground="white", font=("Arial", 12, "bold"))

def on_leave(event):
    widget = event.widget
    widget.config(background="#4CAF50", foreground="white", font=("Arial", 12, "normal"))


root = tk.Tk()
root.title("Activity Tracker")


style = ttk.Style()
style.configure('TFrame', background='#f5f5f5')
style.configure('TButton', background='#4CAF50', foreground='white', font=('Arial', 12, 'bold'))
style.configure('TLabel', background='#f5f5f5', font=('Arial', 12, 'bold'))


main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)


settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
settings_frame.pack(pady=10, fill=tk.X)


interval_label = ttk.Label(settings_frame, text="Screenshot Interval (seconds):")
interval_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
interval_entry = ttk.Entry(settings_frame, width=10)
interval_entry.insert(0, str(config.screenshot_interval))
interval_entry.grid(row=0, column=1, padx=5, pady=5)


blur_var = tk.BooleanVar(value=config.blur_screenshots)
blur_check = ttk.Checkbutton(settings_frame, text="Blur Screenshots", variable=blur_var)
blur_check.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


save_button = ttk.Button(settings_frame, text="Save Settings", command=update_config)
save_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)


button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=10)


start_button = tk.Button(button_frame, text="Start Tracking", command=start_tracking, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
start_button.grid(row=0, column=0, padx=5)
start_button.bind("<Enter>", on_enter)
start_button.bind("<Leave>", on_leave)

stop_button = tk.Button(button_frame, text="Stop Tracking", command=stop_tracking, state=tk.DISABLED, bg="#f44336", fg="white", font=("Arial", 12, "bold"))
stop_button.grid(row=0, column=1, padx=5)
stop_button.bind("<Enter>", on_enter)
stop_button.bind("<Leave>", on_leave)

upload_button = tk.Button(button_frame, text="Manual Upload", command=manual_upload, bg="#2196F3", fg="white", font=("Arial", 12, "bold"))
upload_button.grid(row=0, column=2, padx=5)
upload_button.bind("<Enter>", on_enter)
upload_button.bind("<Leave>", on_leave)

status_label = ttk.Label(main_frame, text="Status: Idle")
status_label.pack(pady=5)

log_frame = ttk.Frame(main_frame)
log_frame.pack(pady=10, fill=tk.BOTH, expand=True)

log_text = tk.Text(log_frame, wrap="word", height=15, width=60, font=("Arial", 10))
log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = Scrollbar(log_frame, command=log_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_text.config(yscrollcommand=scrollbar.set)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        handle_shutdown(None, None)

root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()
