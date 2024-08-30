import pytz
from tzlocal import get_localzone
from datetime import datetime

class TimezoneManager:
    def __init__(self):
        self.current_timezone = get_localzone()

    def check_and_update_timezone(self):
        new_timezone = get_localzone()
        if new_timezone != self.current_timezone:
            print(f"Timezone change detected: {self.current_timezone} -> {new_timezone}")
            self.current_timezone = new_timezone

    def get_current_timestamp(self):
        self.check_and_update_timezone()
        now = datetime.now(self.current_timezone)
        return now.strftime('%Y-%m-%d %H:%M:%S %Z%z')
