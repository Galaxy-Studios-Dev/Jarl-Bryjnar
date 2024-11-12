import discord

class NationEmbed(discord.Embed):
    def __init__(self, querried_nation):
        super().__init__()
        self.title = querried_nation.name()
        self.set_thumbnail(url=querried_nation.flag())
        self.add_field(name="Founded", value=querried_nation.founded())
        self.add_field(name="Avg Score", value=querried_nation.nationScore(), inline=False)
        self.add_field(name="General Stats", value=f"Population: {querried_nation.population()}\nGDP: ${querried_nation.GDP()}", inline=False)

        self.add_field(name="Nation Stats", value=f"Total Cities: {len(querried_nation.cities())}\nInfra/Land: {int(querried_nation.infrastructure())}/{int(querried_nation.land())}", inline=False)
        self.add_field(name="Military Stats", value=f"Total Soldiers: {querried_nation.totalSoldiers()}\nTotal Tanks: {querried_nation.totalTanks()}\nTotal Aircraft: {querried_nation.totalAircraft()}\nTotal Ships: {querried_nation.totalShips()}\nTotal Spies: {querried_nation.totalSpies()}\nTotal Missiles: {querried_nation.totalMissiles()}\nTotal Nukes: {querried_nation.totalNukes()}\n", inline=False)
        self.add_field(name="War Stats", value=f"Wars Won: {querried_nation.warsWon()}\nWars Lost: {querried_nation.warsLost()}\nTotal Wars: {querried_nation.warsWon() + querried_nation.warsLost()}", inline=False)
