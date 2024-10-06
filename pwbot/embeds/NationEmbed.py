import discord


class NationEmbed(discord.Embed):
    def __init__(self, querried_nation):
        super().__init__()
        self.title = querried_nation.getName()
        self.set_thumbnail(url=querried_nation.getFlag())
        self.add_field(name="Founded", value=querried_nation.getFounded())
        self.add_field(name="Avg Score", value=querried_nation.getNationScore(), inline=False)
        self.add_field(name="General Stats", value=f"Population: {querried_nation.getPopulation()}\nGDP: ${querried_nation.getGDP()}", inline=False)

        self.add_field(name="Nation Stats", value=f"Total Cities: {len(querried_nation.getCities())}\nInfra/Land: {int(querried_nation.getInfrastructure())}/{int(querried_nation.getLand())}", inline=False)
        self.add_field(name="Military Stats", value=f"Total Soldiers: {querried_nation.getTotalSoldiers()}\nTotal Tanks: {querried_nation.getTotalTanks()}\nTotal Aircraft: {querried_nation.getTotalAircraft()}\nTotal Ships: {querried_nation.getTotalShips()}\nTotal Spies: {querried_nation.getTotalSpies()}\nTotal Missiles: {querried_nation.getTotalMissiles()}\nTotal Nukes: {querried_nation.getTotalNukes()}\n", inline=False)
        self.add_field(name="War Stats", value=f"Wars Won: {querried_nation.getWarsWon()}\nWars Lost: {querried_nation.getWarsLost()}\nTotal Wars: {querried_nation.getWarsWon() + querried_nation.getWarsLost()}", inline=False)
