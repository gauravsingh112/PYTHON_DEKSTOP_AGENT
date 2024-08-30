import dropbox
import os
import time
import queue
import socket

DROPBOX_ACCESS_TOKEN = 'accces token '
UPLOAD_RETRY_INTERVAL = 60  

class UploadManager:
    def __init__(self):
        self.upload_queue = queue.Queue()

    def check_internet_connection(self):
        try:
            # Try to connect to a well-known public DNS server (Google's DNS)
            socket.create_connection(("8.8.8.8", 53), timeout=10)
            return True
        except socket.timeout:
            print("Internet connection timed out. Possible firewall restriction.")
            return False
        except socket.error:
            print("Failed to connect. Possible firewall issue.")
            return False

    def upload_to_dropbox(self, file_path):
        if not self.check_internet_connection():
            print(f"No internet connection. Queuing {file_path} for later upload.")
            self.upload_queue.put(file_path)
            return

        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

        with open(file_path, "rb") as f:
            file_name = os.path.basename(file_path)
            try:
                dbx.files_upload(f.read(), f'/{file_name}')
                print(f"Uploaded {file_name} to Dropbox")
            except dropbox.exceptions.ApiError as e:
                if isinstance(e.error, dropbox.files.UploadError):
                    print(f"Upload failed: {e.error}. Retrying...")
                    self.upload_queue.put(file_path)
                elif isinstance(e.error, dropbox.auth.AuthError):
                    print(f"Authentication error: {e.error}. Please check your access token.")
                else:
                    print(f"Failed to upload {file_name}: {e}")

    def retry_uploads(self):
        while not self.upload_queue.empty():
            file_path = self.upload_queue.get()
            print(f"Retrying upload for {file_path}...")
            self.upload_to_dropbox(file_path)
            time.sleep(UPLOAD_RETRY_INTERVAL)
