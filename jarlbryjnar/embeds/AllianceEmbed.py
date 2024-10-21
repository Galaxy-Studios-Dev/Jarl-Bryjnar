import discord
from simplepnw.addon.Nation import Nation

class AllianceEmbed(discord.Embed):
    def __init__(self, query):
        super().__init__()
        print("Setting embed info...")
        self.title = f"{query.name()} ({query.acronym()})"
        self.set_thumbnail(url=query.flag())
        self.add_field(name="Founded", value=query.founded())
        self.add_field(name="Avg Score", value=query.averageScore(), inline=False)

        print("Organizing query Stats data... Continuing to General Stats now....")
        general = query.generalStats()
        print("Finished organizing general stats query data... Continuing to War Stats now....")
        wars = query.warStats()
        print("Finished organizing war stats query data... Continuing to Military Stats now....")
        military = query.militaryStats()
        print("Finished organizing military stats query data... Finishing setting up embed info....")

        self.add_field(name="General Stats", value=f"Population: {general['pop']}\nGDP: {general['gdp']}", inline=False)
        self.add_field(name="Nation Stats", value=f"Total Cities: {general['cities']}\nInfra/Land: {general['infra']}/{general['land']}", inline=False)
        self.add_field(name="Military Stats", value=f"Soldiers: {military['soldiers']}\nTanks: {military['tanks']}\nAircraft: {military['aircraft']}\nShips: {military['ships']}\nSpies: {military['spies']}\n", inline=False)
        self.add_field(name="War Stats", value=f"Wars Won: {wars['won']}\nWars Lost: {wars['lost']}\nTotal Wars: {wars['total']}", inline=False)
        print("Finished creating alliance embed...")