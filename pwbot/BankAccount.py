class BankAccount:
    __bank_id = 0

    __cash = 0
    __raw = {'coal': 0, 'iron': 0, 'lead': 0, 'bauxite': 0, 'oil': 0, 'uranium': 0, 'food': 0}
    __manu = {'steel': 0, 'aluminum': 0, 'munitions': 0, 'gasoline': 0}

    def __init__(self, bank_id):
        self.__bank_id = bank_id

    def getBankNumber(self):
        return self.__bank_id

    def getMoney(self):
        return self.__cash

    def getCoal(self):
        return self.__raw['coal']

    def getIron(self):
        return self.__raw['iron']

    def getLead(self):
        return self.__raw['lead']

    def getBauxite(self):
        return self.__raw['bauxite']

    def getOil(self):
        return self.__raw['oil']

    def getUranium(self):
        return self.__raw['uranium']

    def getFood(self):
        return self.__raw['food']

    def getSteel(self):
        return self.__manu['steel']

    def getAluminum(self):
        return self.__manu['aluminum']

    def getMunitions(self):
        return self.__manu['munitions']

    def getGasoline(self):
        return self.__manu['gasoline']

    def updateBalance(self, details):
        self.__cash = details['cash']
        self.__raw = details['raw']
        self.__manu = details['manu']

    def toDict(self):
        return {'id': self.__bank_id, 'cash': self.__cash, 'raw': self.__raw, 'manu': self.__manu}
