import discord


class AuditEmbed(discord.Embed):
    def __init__(self, server, member, required):
        super().__init__()
        if server == 13111:
            self.title = f"{member.getName()} ({len(member.getCities())} Cities)\nRequired: {required}"
            self.description = member.getDiscordUser().mention
            self.set_thumbnail(url=member.getFlag())
        elif server == 13173:
            self.title = f"{member.getName()} ({len(member.getCities())} Cities)\nRequired: {required}"
            self.description = member.getDiscordUser().mention
            self.set_thumbnail(url=member.getFlag())

