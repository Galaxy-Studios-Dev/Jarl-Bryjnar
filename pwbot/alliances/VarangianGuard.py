import os

from simplepnw.queries.Nation import Nation

from pwbot.Alliance import Alliance
from pwbot.utils.FileManager import FileManager

file_manager = FileManager()

class VarangianGuard(Alliance):
    def __init__(self, simplepnw):
        super().__init__(simplepnw, 13173)

        self.getWebhookUrls()['audit'] = "https://discord.com/api/webhooks/1291106096668479620/GwIYLxAqlIuU5Y1EZvm0w4lSU1UumE6YqsMsKATLBRbWSV4rTxOQzpLST8ptotSnPcz2"

        if len(os.listdir(self.getMembersPath())) > 0:
            self.loadSettings()

            file_manager.log(f"Loading {self.getName()} Member's List....")

            members = {}

            for file in os.listdir(self.getMembersPath()):
                discord_id = file.split(".")[0]
                members[discord_id] = file_manager.loadMemberFile(simplepnw, f"vg/{discord_id}")

            self.setMembers(members)

            file_manager.log(f"Finished Successfully loading {len(self.getMembers().keys())} {self.getName()} Member's.... Continuing...")