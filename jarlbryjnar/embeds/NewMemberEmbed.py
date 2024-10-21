import discord

from pwbot.utils.Formatter import Formatter

formatter = Formatter()

class NewMemberEmbed(discord.Embed):
    def __init__(self, aa, nation):
        super().__init__()
        self.set_thumbnail(url=nation.flag())

        if aa == 13111 or aa == "vyo" or aa == "valyrian order":
            self.title = "Valyrian Order Registration Office"
        elif aa == 13173 or aa == "vg" or aa == "varangian guard":
            self.title = "Varangian Guard Registration Office"

        self.add_field(name="Registration Successful", value=formatter.registrationSuccessful(aa, nation))
