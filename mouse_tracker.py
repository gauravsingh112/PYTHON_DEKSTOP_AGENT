from pynput import mouse

class MouseTracker:
    def __init__(self, log_file="activity_log.txt"):
        self.mouse_clicks = 0
        self.log_file = log_file
        self.start_mouse_listener()

    def start_mouse_listener(self):
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.mouse_listener.start()

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.mouse_clicks += 1
            self.log_activity(f"Mouse clicked: {self.mouse_clicks} times")

    def log_activity(self, message):
        with open(self.log_file, "a") as f:
            f.write(message + "\n")

    def get_mouse_clicks(self):
        return self.mouse_clicks
