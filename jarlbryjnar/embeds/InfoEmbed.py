import discord

class InfoEmbed(discord.Embed):
    def __init__(self, discord_avatar):
        super().__init__()
        self.title = "Jarl Bryjnar Info"
        self.set_thumbnail(url=discord_avatar)
        self.add_field(name="Developer", value="BigTallahasee\n")
        self.add_field(name="Created", value="09/16/2024", inline=False)
        self.add_field(name="Description", value="Discord bot specifically for VYO and Extensions, inorder to make takes for Politics and war simpler!", inline=False)