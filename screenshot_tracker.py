import time
from PIL import ImageGrab

class ScreenshotTracker:
    def __init__(self):
        pass

    def capture_screenshot(self):
        timestamp = int(time.time())
        screenshot_path = f"screenshot_{timestamp}.png"

        # Capture the screenshot
        screenshot = ImageGrab.grab()
        screenshot.save(screenshot_path)

        print(f"Screenshot saved at {screenshot_path}")
        return screenshot_path
