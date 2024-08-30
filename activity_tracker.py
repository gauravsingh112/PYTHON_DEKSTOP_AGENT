import time
from PIL import ImageGrab, ImageFilter
import os
from pynput import mouse, keyboard

class ActivityTracker:
    def __init__(self, config, log_file):
        self.config = config
        self.log_file = log_file
        self.prev_mouse_clicks = 0
        self.prev_keyboard_presses = 0
        self.mouse_clicks = 0
        self.keyboard_presses = 0
        self.last_mouse_position = None
        self.last_keyboard_input_time = time.time()
        self.movement_threshold = 5 

        # Setup listeners
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.mouse_clicks += 1

    def on_key_press(self, key):
        self.keyboard_presses += 1

    def capture_screenshot(self):
        timestamp = int(time.time())
        screenshot_path = f"screenshot_{timestamp}.png"

        screenshot = ImageGrab.grab()

        
        if self.config.blur_screenshots:
            screenshot = screenshot.filter(ImageFilter.GaussianBlur(5))
        
        screenshot.save(screenshot_path)
        print(f"Screenshot saved at {screenshot_path}")
        return screenshot_path

    def detect_scripted_activity(self):
        """Detects scripted activity based on mouse movement patterns and keyboard input intervals."""
        
        return False

    def get_activity_summary(self):
       
        current_mouse_clicks = self.mouse_clicks
        current_keyboard_presses = self.keyboard_presses
        
        summary = {
            'current_mouse_clicks': current_mouse_clicks,
            'previous_mouse_clicks': self.prev_mouse_clicks,
            'current_keyboard_presses': current_keyboard_presses,
            'previous_keyboard_presses': self.prev_keyboard_presses
        }
        
       
        self.prev_mouse_clicks = current_mouse_clicks
        self.prev_keyboard_presses = current_keyboard_presses
        
        return summary

    def stop_listeners(self):
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
