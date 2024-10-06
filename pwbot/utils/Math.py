class Math:
    def __init__(self):
        pass

    def totalImps(self, cities):
        return {'barracks': cities * 5, 'factories': cities * 5, 'hangars': cities * 5, 'drydocks': cities * 3}

    def totalUnits(self, total_imps):
        return {'soldiers': total_imps['barracks'] * 3000, 'tanks': total_imps['factories'] * 250, 'planes': total_imps['hangars'] * 15, 'ships': total_imps['drydocks'] * 5}

    def defaultImpTotal(self, cities):
        return cities * 5

    def drydockTotal(self, cities):
        return cities * 3

    def totalSoldiers(self, barracks):
        return barracks * 3000

    def totalTanks(self, factories):
        return factories * 250

    def totalPlanes(self, hangars):
        return hangars * 15

    def totalShips(self, drydocks):
        return drydocks * 5

    def soldierConsumption(self, soldiers):
        return (soldiers / 5000) * 1

    def tankConsumption(self, tanks):
        return (tanks / 250) * 1

    def groundConsumption(self, soldiers, tanks):
        total_munis = soldiers['munis'] + tanks['munis']
        total_gas = soldiers['gas'] + tanks['gas']
        return {'munis': total_munis, 'gas': total_gas}

    def airConsumption(self, planes):
        return (planes / 4) * 1

    def shipMuniConsumption(self, ships):
        return ships * 2.5

    def shipGasConsumption(self, ships):
        return ships * 1.5
