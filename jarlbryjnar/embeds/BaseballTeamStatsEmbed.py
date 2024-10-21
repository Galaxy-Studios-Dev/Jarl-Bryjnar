import discord


class BaseballTeamStatsEmbed(discord.Embed):
    def __init__(self, baseball_team):
        super().__init__()
        self.title = baseball_team.name
        self.set_thumbnail(url=baseball_team.logo)
        self.add_field(name="Stadium", value=f"{baseball_team.stadium}")
        self.add_field(name="Stats", value=f"Wins: {baseball_team.wins}\t\tLosses: {baseball_team.glosses}\t\tTotal Played: {baseball_team.games_played}\nHomers: {baseball_team.homers}\t\tStrikeouts: {baseball_team.strikeouts}", inline=False)
