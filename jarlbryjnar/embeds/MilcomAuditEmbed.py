import discord

class MilcomAuditEmbed(discord.Embed):
    def __init__(self, server, member, required):
        super().__init__()
        query = member.get()

        if server == 13111:
            self.title = f"{query.name()} ({len(query.cities())} Cities)\nRequired: {required['barracks']}{required['factories']}{required['hangars']}{required['drydocks']}"
            self.set_thumbnail(url=query.flag())

            audit = member.checkMMR(required)
            temp = audit.copy()

            for key in temp:
                if temp[key] == "passed":
                    del audit[key]
                else:
                    self.add_field(name=key, value=audit[key])

            print(len(self.fields))

            if len(self.fields) > 0:
                self.description = member.discord().mention
            else:
                self.add_field(name="", value="You have passed the Milcom audit! Great work!")

        elif server == 13173:
            self.title = f"{query.name()} ({len(query.cities())} Cities)\nRequired: {required['barracks']}{required['factories']}{required['hangars']}{required['drydocks']}"
            self.set_thumbnail(url=query.flag())

            audit = member.checkMMR(required)
            for key in audit:
                if audit[key] == "passed":
                    pass
                else:
                    self.add_field(name=key, value=audit[key])

            if len(self.fields) > 0:
                self.description = member.discord().mention
            else:
                self.add_field(name="", value="You have passed the Milcom audit! Great work!")