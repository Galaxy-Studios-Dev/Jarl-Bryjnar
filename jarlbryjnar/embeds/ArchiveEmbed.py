import discord

class ArchiveEmbed(discord.Embed):
    __pw_rules = "https://politicsandwar.com/rules/"
    __pw_terminology = "https://politicsandwar.com/pwpedia/article/Terminology-Glossary"

    __welcome_to_vyo = "https://docs.google.com/document/d/1qUXNQV9tTNxHz-3xS0ffA4bi1qPzCXB6Q9FANbJ9G1g/edit"
    __vyo_basics = "https://docs.google.com/document/d/12jD-d9sp7i9u9UK9vt_lHuMsUFRvHNbEV7z4fjHu5K0/edit?usp=sharing"

    __welcome_to_rdh = ""
    __rdh_basics = ""

    __welcome_to_vg = "https://docs.google.com/document/d/1kHqOQeq6aHS_OvWe8KUZMNn3od7U3a8nHTqBEXA1Vy0/edit?usp=sharing"
    __vg_basics = "https://docs.google.com/document/d/1l52NrjGjTA4W3YwIj4lZUR9BC9bgxYYz21FZFPScpaQ/edit?usp=sharing"

    __welcome_to_mf = "https://docs.google.com/document/d/17hDn8eHLQF_QPTYn2qO9eET0rjB3P44s1hZy9Cp2Wk8/edit?usp=sharing"
    __mf_basics = "https://docs.google.com/document/d/1X3aUF6aZGymnKYZgq6FHgG_onbQawD80coLyzmHF6oY/edit?usp=sharing"

    __vyo_thumbnail = "C://Users/gam3r/Discord Bots/pwbots/imgs/library2.png"
    __rdh_thumbnail = "C://Users/gam3r/Discord Bots/pwbots/imgs/library4.png"
    __vg_thumbnail = "C://Users/gam3r/Discord Bots/pwbots/imgs/library1.png"
    __mf_thumbnail = "C://Users/gam3r/Discord Bots/pwbots/imgs/library3.png"

    __file = ""

    def __init__(self, aa_id):
        super().__init__()

        if aa_id == 13111:
            self.title = "The Library of Reykjavik"
            self.set_thumbnail(url="attachment://Users/gam3r/Discord Bots/pwbots/imgs/library2.png")
            self.add_field(name="Politics and War", value=f"Rules\n[Click Here]({self.__pw_rules})\nTerminology\n[Click Here]({self.__pw_terminology})")
            self.add_field(name="Guides", value=f"Handbook\n[Click Here]({self.__welcome_to_vyo})\nBasic Training\n[Click Here]({self.__vyo_basics})", inline=False)
            self.__file = discord.File(self.__vyo_thumbnail, filename='library2.png')
        elif aa_id == 13173:
            self.title = "The Library of Neo Azora"
            self.set_thumbnail(url="attachment://Users/gam3r/Discord Bots/pwbots/imgs/library1.png")
            self.add_field(name="Politics and War",
                           value=f"Rules\n[Click Here]({self.__pw_rules})\nTerminology\n[Click Here]({self.__pw_terminology})")
            self.add_field(name="Guides", value=f"Handbook\n[Click Here]({self.__welcome_to_vg})\nBasic Training\n[Click Here]({self.__vg_basics})", inline=False)
            self.__file = discord.File(self.__vg_thumbnail, filename='library1.png')
        elif aa_id == 1 or aa_id == "monarchs fellowship":
            self.title = "The Library of Kaiserreich Africa"
            self.set_thumbnail(url="attachment://Users/gam3r/Discord Bots/pwbots/imgs/library4.png")
            self.add_field(name="Politics and War",
                           value=f"Rules\n[Click Here]({self.__pw_rules})\nTerminology\n[Click Here]({self.__pw_terminology})")
            self.add_field(name="Guides", value=f"Handbook\n[Click Here]({self.__welcome_to_mf})\nBasic Training\n[Click Here]({self.__mf_basics})", inline=False)
            self.__file = discord.File(self.__mf_thumbnail, filename='library4.png')

    def getFile(self):
        return self.__file
