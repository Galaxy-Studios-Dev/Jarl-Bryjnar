import discord

class NewMemberEmbed(discord.Embed):
    def __init__(self, aa, nation):
        super().__init__()
        self.set_thumbnail(url=nation.flag())
        alliance = ""

        if aa == 13111 or aa == "vyo" or aa == "valyrian order":
            self.title = "Valyrian Order Registration Office"
            alliance = "Valyrian Order"
        elif aa == 13173 or aa == "vg" or aa == "varangian guard":
            self.title = "Varangian Guard Registration Office"
            alliance = "Varangian Guard"

        self.add_field(name="Registration Successful", value=f"{nation.get().name()} was registered successfully to {alliance}!")
