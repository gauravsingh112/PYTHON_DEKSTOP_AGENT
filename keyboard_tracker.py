from pynput import keyboard

class KeyboardTracker:
    def __init__(self, log_file="activity_log.txt"):
        self.keyboard_presses = 0
        self.log_file = log_file
        self.start_keyboard_listener()

    def start_keyboard_listener(self):
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.keyboard_listener.start()

    def on_press(self, key):
        self.keyboard_presses += 1
        self.log_activity(f"Key pressed: {self.keyboard_presses} times")

    def log_activity(self, message):
        with open(self.log_file, "a") as f:
            f.write(message + "\n")

    def get_keyboard_presses(self):
        return self.keyboard_presses
