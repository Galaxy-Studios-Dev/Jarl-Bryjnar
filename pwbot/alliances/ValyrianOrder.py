import os

from simplepnw.queries.Nation import Nation

from pwbot.Alliance import Alliance
from pwbot.utils.FileManager import FileManager

file_manager = FileManager()

class ValyrianOrder(Alliance):
    def __init__(self, simplepnw):
        super().__init__(simplepnw, 13111)

        self.getWebhookUrls()['audit'] = "https://discord.com/api/webhooks/1291118659074265220/pUHVxYeS8LAnQ7jvmah0M59xZjmAMupXAJKciLp0F3a33V3QoRSRYxlU9u9cjEYgjH-q"

        if len(os.listdir(self.getMembersPath())) > 0:
            self.loadSettings()

            file_manager.log(f"Loading {self.getName()} Member's List....")

            members = {}

            for file in os.listdir(self.getMembersPath()):
                discord_id = file.split(".")[0]
                members[discord_id] = file_manager.loadMemberFile(simplepnw, f"vyo/{discord_id}")

            self.setMembers(members)

            file_manager.log(f"Finished Successfully loading {len(self.getMembers().keys())} {self.getName()} Member's.... Continuing...")
