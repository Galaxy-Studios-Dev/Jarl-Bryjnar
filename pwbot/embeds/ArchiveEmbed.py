import discord


class ArchiveEmbed(discord.Embed):
    __pw_rules = "https://politicsandwar.com/rules/"
    __pw_terminology = "https://politicsandwar.com/pwpedia/article/Terminology-Glossary"
    __vyo_doc_hub = "https://docs.google.com/document/d/1qUXNQV9tTNxHz-3xS0ffA4bi1qPzCXB6Q9FANbJ9G1g/edit"
    __vg_doc_hub = "https://docs.google.com/document/d/1ok-WRLjFfAEhylVCI3TdRZRQlIwCmZju0Pzg6IBGjdE/edit"

    __vyo_thumbnail = "C://Users/gam3r/Discord Bots/pwbots/imgs/library2.png"
    __vg_thumbnail = "C://Users/gam3r/Discord Bots/pwbots/imgs/library1.png"
    __file = ""

    def __init__(self, aa_id):
        super().__init__()

        if aa_id == 13111:
            self.title = "The Library of Reykjavik"
            self.set_thumbnail(url="attachment://Users/gam3r/Discord Bots/pwbots/imgs/library2.png")
            self.add_field(name="Politics and War", value=f"Rules\n[Click Here]({self.__pw_rules})\nTerminology\n[Click Here]({self.__pw_terminology})")
            self.add_field(name="Guides", value=f"Doc Hub\n[Click Here]({self.__vyo_doc_hub})", inline=False)
            self.__file = discord.File(self.__vyo_thumbnail, filename='library2.png')
        elif aa_id == 13173:
            self.title = "The Library of Neo Azora"
            self.set_thumbnail(url="attachment://Users/gam3r/Discord Bots/pwbots/imgs/library1.png")
            self.add_field(name="Politics and War",
                           value=f"Rules\n[Click Here]({self.__pw_rules})\nTerminology\n[Click Here]({self.__pw_terminology})")
            self.add_field(name="Guides", value=f"Doc Hub\n[Click Here]({self.__vg_doc_hub})", inline=False)
            self.__file = discord.File(self.__vg_thumbnail, filename='library1.png')

    def getFile(self):
        return self.__file
