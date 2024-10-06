import os

import discord
from simplepnw.queries.Nation import Nation

from pwbot.utils.FileManager import FileManager

file_manager = FileManager()

class Alliance:
    __kit = {}
    __id = 0

    __discord_server = 0

    __discord_role_ids = {}
    __webhook_urls = {}

    __members_path = ""
    __members = {}

    __required_mmr = {"production": {'barracks': 0, 'factories': 0, 'hangars': 0, 'drydocks': 0},
                      "raider": {'barracks': 0, 'factories': 0, 'hangars': 0, 'drydocks': 0}}

    def __init__(self, simplepnw, aa_id):
        self.__kit = simplepnw
        self.__name = ""
        self.__id = int(aa_id)

        settings = file_manager.loadJson(f"{file_manager.default_path}{self.__id}")
        self.__discord_role_ids = settings['discord_role_ids']

        if aa_id == 13111:
            self.__name = "Valyrian Order"
            self.__members_path = f"{file_manager.default_path}members/vyo/"

        elif aa_id == 13173:
            self.__name = "Varangian Guard"
            self.__members_path = f"{file_manager.default_path}members/vg/"

    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def getDiscordServer(self):
        return self.__discord_server

    def LEADER(self, action):
        role = discord.utils.get(action.guild.roles, id=self.__discord_role_ids["LEADER"])
        return role

    def HEADDEPT(self, action):
        role = discord.utils.get(action.guild.roles, id=self.__discord_role_ids["HEADDEPT"])
        return role

    def FA(self, action):
        role = discord.utils.get(action.guild.roles, id=self.__discord_role_ids["FA"])
        return role

    def IA(self, action):
        role = discord.utils.get(action.guild.roles, id=self.__discord_role_ids["IA"])
        return role

    def MILCOM(self, action):
        role = discord.utils.get(action.guild.roles, id=self.__discord_role_ids["MILCOM"])
        return role

    def ECON(self, action):
        role = discord.utils.get(action.guild.roles, id=self.__discord_role_ids["ECON"])
        return role

    def ECONNB(self, action):
        role = discord.utils.get(action.guild.roles, id=self.__discord_role_ids["ECONNB"])
        return role

    def MEMBER(self, action):
        role = discord.utils.get(action.guild.roles, id=self.__discord_role_ids["MEMBER"])
        return role

    def getWebhookUrls(self):
        return self.__webhook_urls

    def getWebhookUrl(self, key):
        return self.__webhook_urls[key]

    def getMembersPath(self):
        return self.__members_path

    def getMembers(self):
        return self.__members

    def setMembers(self, value):
        self.__members = value

    def getMMR(self, key):
        return self.__required_mmr[key]

    def setMMR(self, key, values):
        if key == "raider" or key == "production":
            current = self.__required_mmr[key]

            self.__required_mmr[key]['barracks'] = values['barracks']
            self.__required_mmr[key]['factories'] = values['factories']
            self.__required_mmr[key]['hangars'] = values['hangars']
            self.__required_mmr[key]['drydocks'] = values['drydocks']

    def formatMMR(self, key):
        return f"{self.getMMR(key)['barracks']}{self.getMMR(key)['factories']}{self.getMMR(key)['hangars']}{self.getMMR(key)['drydocks']}"

    def loadSettings(self):
        settings = file_manager.loadAASettingsFile(self.__id)
        self.__discord_server = int(settings['discord_server'])
        self.__discord_role_ids = settings['discord_role_ids']
        self.__required_mmr = settings['mmr_reqs']

    def toDict(self):
        return {"aa_id": self.__id, "members": self.__members}
