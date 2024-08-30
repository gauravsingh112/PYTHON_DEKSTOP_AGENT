import pytz
from tzlocal import get_localzone

class Config:
    def __init__(self):
        self.screenshot_interval = 300  # Screenshot every 5 minutes
        self.blur_screenshots = False
        self.timezone = get_localzone()

    def update_timezone(self):
        self.timezone = get_localzone()
        print(f"Timezone updated to: {self.timezone}")
