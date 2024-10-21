import datetime
import json
import os.path

from pwbot.utils.Formatter import Formatter

formatter = Formatter()

class Logger:
    default_path = ""
    log_path = f"{default_path}logs/"

    def __init__(self, default_path):
        self.default_path = default_path

    def log(self, content):
        today = datetime.datetime.now()

        current_log = f"{self.log_path}{self.formatDate(today)}.log"
        if os.path.exists(current_log):
            file = open(current_log, 'a')
            file.write(f"[Jarl Bryjnar]{self.formatTime(today)} ~> {content}\n")

            file.close()
        else:
            file = open(current_log, "w")
            file.write(f"[Jarl Bryjnar]{self.formatTime(today)} ~> {content}\n")

            file.close()

    def formatTime(self, time):
        total_time = ""

        if time.hour < 10:
            hour = f"0{time.hour}"

            if time.minute < 10:
                minutes = f"0{time.minute}"

                if time.second < 10:
                    seconds = f"0{time.second}"
                    return f"{time.hour}:{time.minute}:{time.second}"
        else:
            hour = f"{time.hour}"
            if time.minute > 10:
                minutes = f"{time.minute}"
                if time.second > 10:
                    seconds = f"{time.second}"
                    return f"{hour}:{minutes}:{seconds}"

    def formatDate(self, date):
        return f"{date.month}-{date.day}-{date.year}"
