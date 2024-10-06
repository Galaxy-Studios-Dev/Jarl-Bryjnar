import discord

from pwbot.utils.Formatter import Formatter

formatter = Formatter()

class NewMemberEmbed(discord.Embed):
    def __init__(self, aa, query):
        super().__init__()
        self.set_thumbnail(url=query.getFlag())

        if aa == 13111 or aa == "vyo" or aa == "valyrian order":
            self.title = "Valyrian Order"
        elif aa == 13173 or aa == "vg" or aa == "varangian guard":
            self.title = "Varangian Guard"

        self.add_field(name="Registration Successful", value=formatter.registrationSuccessful(aa, query))
