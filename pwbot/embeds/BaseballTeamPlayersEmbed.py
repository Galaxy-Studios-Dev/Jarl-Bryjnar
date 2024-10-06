import discord


class BaseballTeamPlayersEmbed(discord.Embed):
    def __init__(self, baseball_team):
        super().__init__()
        self.title = baseball_team.name
        self.set_thumbnail(url=baseball_team.logo)

        players = ""

        for player in baseball_team.players:
            temp = f"\n{player.name}\nAge: {player.age}\nBirthday: {player.birthday} turns\nPosition: {player.position}\nOverall: {player.overall}\n"
            players = players + temp

        self.add_field(name="Players", value=players, inline=False)
