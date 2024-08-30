import time
from activity_tracker import ActivityTracker
from data_upload import UploadManager  
from config import Config
import signal
import sys

def handle_shutdown(signum, frame):
    print("Shutting down gracefully...")
    upload_manager.retry_uploads()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_shutdown)  
signal.signal(signal.SIGTERM, handle_shutdown) 

def main():
    config = Config()
    tracker = ActivityTracker(config, log_file="activity_log.txt")
    global upload_manager
    upload_manager = UploadManager()

    while True:
        try:
            
            screenshot_path = tracker.capture_screenshot()

            
            activity_summary = tracker.get_activity_summary()
            print(f"Activity Summary: {activity_summary}")

            
            upload_manager.upload_to_dropbox(screenshot_path)

           
            time.sleep(config.screenshot_interval)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
