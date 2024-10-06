import datetime
import json
import os.path

from simplepnw.queries.Nation import Nation
from pwbot.BankAccount import BankAccount
from pwbot.utils.Formatter import Formatter

formatter = Formatter()

class FileManager:
    default_path = "C:/Users/gam3r/Discord Bots/pwbots/"
    log_path = f"{default_path}logs/"

    members_path = f"{default_path}members/"
    bank_path = f"{default_path}/treasury/"

    def __init__(self):
        pass

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

    def loadJson(self, path):
        if os.path.isdir(path):
            return {"discord_id": 0, "nation_id": 0}
        else:
            file = open(f"{path}.json", 'r')
            data = json.load(file)
            file.close()

            return data

    def saveJson(self, path, data):
        file = open(f"{path}.json", 'w')
        json.dump(data, file)
        file.close()

    def createAASettingsFile(self, aa_id, details):
        aa_settings_path = f"{self.default_path}{aa_id}"
        self.saveJson(aa_settings_path, details)

    def loadAASettingsFile(self, aa_id):
        aa_settings_path = f"{self.default_path}{aa_id}"

        if os.path.exists(f"{aa_settings_path}.json"):
            return self.loadJson(aa_settings_path)

    def createMemberFile(self, simplepnw, path, details):
        member_path = f"{self.members_path}{path}"
        self.saveJson(member_path, {'discord': details['discord'].id, 'nation_id': details['nation_id']})
        self.createBankFile(path, BankAccount(details['discord'].id).toDict())

        nation = Nation(simplepnw, details['nation_id'])
        nation.setDiscord(details['discord'])
        return nation

    def loadMemberFile(self, simplepnw, path):
        member_path = f"{self.members_path}{path}.json"
        discord_id = path.split("/")[1].split(".")[0]

        if os.path.exists(member_path):
            data = self.loadJson(member_path.split(".")[0])
            nation = Nation(simplepnw, int(data['nation_id']))
            nation.setDiscordId(int(discord_id))
            return nation

    def createBankFile(self, path, details):
        bank_path = f"{self.bank_path}{path}"
        self.saveJson(bank_path, details)

    def loadBankFile(self, path):
        bank_path = f"{self.default_path}treasury/{path}"

        if os.path.exists(bank_path):
            data = self.loadJson(bank_path)
