import datetime

class Logger:
    def __init__(self, filename):
        self.filename = filename

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
        log_message = f"[{timestamp}] {message}\n"
        with open(self.filename, 'a') as f:
            f.write(log_message)

