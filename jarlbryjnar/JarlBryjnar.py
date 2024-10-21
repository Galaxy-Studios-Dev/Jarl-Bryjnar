import datetime
import os.path

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from simplepnw.SimplePnW import SimplePnW

from simplepnw.addon.Alliance import Alliance
from simplepnw.addon.Nation import Nation
from simplepnw.queries.AllianceQuery import AllianceQuery
from simplepnw.queries.NationQuery import NationQuery

from pwbot.embeds.ActivityAuditEmbed import ActivityAuditEmbed
from pwbot.embeds.AllianceEmbed import AllianceEmbed
from pwbot.embeds.ArchiveEmbed import ArchiveEmbed
from pwbot.embeds.MilcomAuditEmbed import MilcomAuditEmbed
from pwbot.embeds.InfoEmbed import InfoEmbed
from pwbot.embeds.NationEmbed import NationEmbed
from pwbot.embeds.NewMemberEmbed import NewMemberEmbed

from pwbot.utils.Logger import Logger
from pwbot.utils.Formatter import Formatter
from pwbot.utils.RoleIds import RoleIds

formatter = Formatter()

role_ids = RoleIds()

class JarlBryjnar:
    __token = ""
    __kit = ""
    __logger = {}

    __default_path = "Discord Bots/pwbots/"

    __vyo = {}
    __vg = {}
    # __rdh = {}

    def __init__(self, token):
        self.__token = token
        self.__kit = SimplePnW("f1e65cb20de0af9c1ede", self.__default_path, True)
        self.__logger = Logger(self.__kit.dataManager().logger_path)

        self.__vyo = Alliance(self.__kit, 13111)
        self.__vyo.createDirectory()

        self.__vg = Alliance(self.__kit, 13173)
        self.__vg.createDirectory()

        # self.__mf = Alliance(self.__kit, 0)
        # self.__mf.createDirectory()
        # self.__mf.setup()

    def run(self):
        bot = commands.Bot(command_prefix=['$', '!'], intents=discord.Intents.all())

        @bot.event
        async def on_ready():
            vyo_guild = bot.get_guild(1278478363400339481)
            vg_guild = bot.get_guild(1283514897224958003)
            #mf_guild = bot.get_guild()

            self.__vyo.setDiscord(vyo_guild)
            self.__vg.setDiscord(vg_guild)
            # self.__vg.setDiscord(mf_guild)

            self.__vyo.setup()
            self.__vg.setup()

            try:
                synced = await bot.tree.sync()
                print(f"Synced {len(synced)} command(s)")
            except Exception as e:
                print(e)

        @bot.event
        async def on_disconnect():
            self.__vyo.save()
            self.__vg.save()
            # self.__mf.save()

        @bot.tree.command(name="archive")
        @app_commands.describe(alliance="which alliance to access")
        @app_commands.choices(alliance=[
                app_commands.Choice(name="Valyrian Order", value=13111),
                app_commands.Choice(name="Varangian Guard", value=13173),
                app_commands.Choice(name="Test Alliance", value=1)
            ]
        )
        async def archive(interaction: discord.Interaction, alliance: app_commands.Choice[int]):
            embed = ArchiveEmbed(alliance.value)
            file = embed.getFile()
            await interaction.response.send_message(file=file, embed=embed)

        @bot.tree.command(name="audit")
        @app_commands.describe(audit_type="What type of audit to run", alliance="What alliance to audit")
        @app_commands.choices(audit_type=[
                app_commands.Choice(name="Milcom", value="milcom"),
                app_commands.Choice(name="Activity", value='activity')
            ],
                alliance=[
                app_commands.Choice(name="Valyrian Order", value=13111),
                app_commands.Choice(name="Varangian Guard", value=13173),
                app_commands.Choice(name="Test Alliance", value=1)
            ]
        )
        async def audit(interaction: discord.Interaction, audit_type: app_commands.Choice[str], alliance: app_commands.Choice[int]):
            roles = interaction.user.roles

            followup = interaction.followup

            if self.__vyo.LEADER(interaction) in roles or self.__vyo.MILCOM(interaction) in roles or self.__vg.LEADER(interaction) in roles or self.__vg.MILCOM(interaction) in roles:
                if audit_type.value == "milcom":
                    if alliance.value == 13111:
                        self.__vyo.addWebhookUrl('audit', "https://discord.com/api/webhooks/1291106096668479620/GwIYLxAqlIuU5Y1EZvm0w4lSU1UumE6YqsMsKATLBRbWSV4rTxOQzpLST8ptotSnPcz2")

                        for member in self.__vyo.members():
                            discord_user = discord.utils.get(interaction.guild.members, id=int(member))
                            member = self.__vyo.members()[member]
                            member.setDiscord(discord_user)

                            if len(member.get().cities()) >= 16:
                                mmr_key = 'production'
                                required_mmr = self.__vyo.specificMMR(mmr_key)
                                embed = MilcomAuditEmbed(alliance.value, member, required_mmr)
                            elif len(member.get().cities()) < 16:
                                mmr_key = 'raider'
                                required_mmr = self.__vyo.specificMMR(mmr_key)
                                embed = MilcomAuditEmbed(alliance.value, member, required_mmr)
                            async with aiohttp.ClientSession() as session:
                                webhook_url = self.__vyo.webhookUrl('audit')
                                webhook = followup.from_url(webhook_url, session=session)
                                await webhook.send(embed=embed, username='Jarl Bryjnar')
                        return
                    elif alliance.value == 13173:
                        self.__vg.addWebhookUrl('audit',"https://discord.com/api/webhooks/1291118659074265220/pUHVxYeS8LAnQ7jvmah0M59xZjmAMupXAJKciLp0F3a33V3QoRSRYxlU9u9cjEYgjH-q")

                        for member in self.__vg.members():
                            discord_user = discord.utils.get(interaction.guild.members, id=int(member))
                            member = self.__vg.members()[member]
                            member.setDiscord(discord_user)

                            if len(member.get().cities()) >= 16:
                                required_mmr = self.__vg.specificMMR("production")
                                embed = MilcomAuditEmbed(alliance.value, member, required_mmr)
                            elif len(member.get().cities()) < 16:
                                required_mmr = self.__vg.specificMMR("raider")
                                embed = MilcomAuditEmbed(alliance.value, member, required_mmr)
                            async with aiohttp.ClientSession() as session:
                                webhook_url = self.__vg.webhookUrl('audit')
                                webhook = followup.from_url(webhook_url, session=session)
                                await webhook.send(embed=embed, username='Jarl Bryjnar')
                        return
                    elif alliance.value == 1:
                        pass
                elif audit_type.value == ("activity"):
                    if alliance.value == 13111:
                        self.__vyo.addWebhookUrl('audit', "https://discord.com/api/webhooks/1291106096668479620/GwIYLxAqlIuU5Y1EZvm0w4lSU1UumE6YqsMsKATLBRbWSV4rTxOQzpLST8ptotSnPcz2")
                        members = self.__vyo.members()

                        for member in members:
                            discord_user = discord.utils.get(interaction.guild.members, id=int(member))
                            member = members[member]
                            member.setDiscord(discord_user)

                            current_day = datetime.datetime.now().day
                            last_day = member.get().lastActive().day

                            days_inactive = int(current_day) - int(last_day)

                            embed = ActivityAuditEmbed(alliance.value, member, member.get().lastActive(), days_inactive)

                            async with aiohttp.ClientSession() as session:
                                webhook_url = self.__vyo.webhookUrl('audit')  # "https://discord.com/api/webhooks/1291106096668479620/GwIYLxAqlIuU5Y1EZvm0w4lSU1UumE6YqsMsKATLBRbWSV4rTxOQzpLST8ptotSnPcz2"
                                webhook = followup.from_url(webhook_url, session=session)
                                await webhook.send(embed=embed, username='Jarl Bryjnar')
                    elif alliance.value == 13173:
                        members = self.__vg.members()

                        for member in members:
                            member = members[member]

                            discord_user = discord.utils.get(interaction.guild.members, id=int(member))
                            member.setDiscord(discord_user)

                            current_day = datetime.datetime.now().day
                            last_day = member.get().lastActive().day

                            days_inactive = current_day - last_day
                            if days_inactive > 2:
                                embed = ActivityAuditEmbed(alliance.value, member, days_inactive)
                            else:
                                embed = ActivityAuditEmbed(alliance.value, member, days_inactive)

                            async with aiohttp.ClientSession() as session:
                                webhook_url = self.__vyo.webhookUrl('audit')  # "https://discord.com/api/webhooks/1291106096668479620/GwIYLxAqlIuU5Y1EZvm0w4lSU1UumE6YqsMsKATLBRbWSV4rTxOQzpLST8ptotSnPcz2"
                                webhook = followup.from_url(webhook_url, session=session)
                                await webhook.send(embed=embed, username='Jarl Bryjnar')
                    elif alliance.value == 1:
                        pass

        @bot.tree.command(name="info")
        async def info(interaction: discord.Interaction):
            bigt = discord.utils.get(interaction.guild.members, id=1177716521573818398)
            embed = InfoEmbed(bigt.avatar.url)
            await interaction.response.send_message(embed=embed)

        @bot.tree.command(name="register")
        @app_commands.describe(alliance="The alliance you are in", nation_id="Id of nation to register")
        @app_commands.choices(alliance=[
            app_commands.Choice(name="Valyrian Order", value=13111),
            app_commands.Choice(name="Varangian Guard", value=13173),
            app_commands.Choice(name="Test Alliance", value=1)
        ])
        async def register(interaction: discord.Interaction, alliance: app_commands.Choice[int], nation_id: int):
            nation = Nation(self.__kit, nation_id)
            nation.setDiscord(interaction.user)

            if alliance.value == 13111 and nation.get().alliance().name == "Valyrian Order":
                self.__vyo.addMember(nation.discordId(), nation)
                self.__vyo.save()

                await interaction.user.add_roles(self.__vyo.MEMBER(interaction))
                await interaction.response.send_message(embed=NewMemberEmbed(alliance.value, nation.get()))
                return
            elif alliance.value == 13173 and nation.get().alliance().name == "Varangian Guard":
                self.__vg.addMember(nation.discordId(), nation)
                self.__vg.save()

                await interaction.user.add_roles(self.__vg.MEMBER(interaction))
                await interaction.response.send_message(embed=NewMemberEmbed(alliance.value, nation.get()))
                return
            elif alliance.value == 1:
                pass

        @bot.tree.command(name="view")
        @app_commands.describe(alliance="whether or not it is a alliance", given_id="Id of nation / alliance to lookup")
        @app_commands.choices(alliance=[
                app_commands.Choice(name="True", value=1),
                app_commands.Choice(name="False", value=0)
            ]
        )
        async def view(interaction: discord.Interaction, alliance: app_commands.Choice[int], given_id: int):
            if alliance.value == 1:
                await interaction.response.defer()
                embed = AllianceEmbed(AllianceQuery(self.__kit, given_id))
                await interaction.followup.send(embed=embed)
                print(f"Response: Pass\nTime: {int(round(bot.latency * 1000))} ms")
            elif alliance.value == 0:
                await interaction.response.defer()
                embed = NationEmbed(NationQuery(self.__kit, given_id))
                await interaction.followup.send(embed=embed)

        @bot.command(
            command_prefix=["!"]
        )
        async def admin(ctx, *args):
            roles = ctx.author.roles

            if self.__vyo.LEADER(ctx) in roles or self.__vg.LEADER(ctx) in roles or ctx.author.global_name == self.__vyo.discord().owner.global_name:
                if args[0] == "set":
                    if args[1] == "mmr":
                        alliance = args[2]
                        mmr_type = args[3]
                        required = args[4].split(",")
                        temp = {}

                        for x in range(len(required)):
                            wanted_value = int(required[x].split("=")[1])

                            if "b" in required[x]:
                                temp['barracks'] = wanted_value
                            elif "f" in required[x]:
                                temp['factories'] = wanted_value
                            elif "h" in required[x]:
                                temp['hangars'] = wanted_value
                            elif "d" in required[x]:
                                temp['drydocks'] = wanted_value

                        print(temp.keys())

                        if mmr_type == "production" or mmr_type == "raider":
                            if int(alliance) == 13111 or alliance == "valyrian order" or alliance == "vyo":
                                self.__vyo.setSpecificMMR(mmr_type, temp)
                                self.__vyo.save()
                            elif int(alliance) == 13173 or alliance == "varangian guard" or alliance == "vg":
                                pass
                    elif args[1] == "role":
                        alliance = args[2]
                        bot_role = args[3]
                        role_id = int(args[4])

                        if int(alliance) == 13111 or alliance == "valyrian order" or alliance == "vyo":
                            if bot_role in self.__vyo.discordRoleIds().keys():
                                previous_role_id = self.__vyo.discordRoleIds()[bot_role]
                                self.__vyo.setSpecificDiscordRole(bot_role, role_id)
                                self.__vyo.save()

                                await ctx.send(f"You have successfully changed {bot_role} to {role_id} [last value ~> {previous_role_id}]")
                            else:
                                await ctx.send(f"Ignoring....")
                        elif int(alliance) == 13173 or alliance == "varangian guard" or alliance == "vg":
                            if bot_role in self.__vg.discordRoleIds().keys():
                                previous_role_id = self.__vg.discordRoleIds()[bot_role]
                                self.__vg.setSpecificDiscordRole(bot_role, role_id)
                                self.__vg.save()

                                await ctx.send(f"You have successfully changed {bot_role} to {role_id} [last value ~> {previous_role_id}]")
                            else:
                                await ctx.send(f"Ignoring....")
                elif args[0] == "view":
                    if args[1] == "discord_roles":
                        alliance = args[2]

                        if alliance.isdigit():
                            if int(alliance) == 13111:
                                await ctx.send(f"LEADER: {self.__vyo.LEADER(ctx).id}\nHEADDEPT: {self.__vyo.HEADDEPT(ctx).id}\nFA: {self.__vyo.FA(ctx).id}\nIA: {self.__vyo.IA(ctx).id}\nMILCOM: {self.__vyo.MILCOM(ctx).id}\nECON: {self.__vyo.ECON(ctx).id}\nECONNB: {self.__vyo.ECONNB(ctx).id}\nMEMBER: {self.__vyo.MEMBER(ctx).id}")
                            elif int(alliance) == 13173:
                                await ctx.send(f"LEADER: {self.__vg.LEADER(ctx).id}\nHEADDEPT: {self.__vg.HEADDEPT(ctx).id}\nFA: {self.__vg.FA(ctx).id}\nIA: {self.__vg.IA(ctx).id}\nMILCOM: {self.__vg.MILCOM(ctx).id}\nECON: {self.__vg.ECON(ctx).id}\nECONNB: {self.__vg.ECONNB(ctx).id}\nMEMBER: {self.__vg.MEMBER(ctx).id}")
                        else:
                            if alliance == "valyrian order" or alliance == "vyo":
                                await ctx.send(f"LEADER: {self.__vyo.LEADER(ctx).id}\nHEADDEPT: {self.__vyo.HEADDEPT(ctx).id}\nFA: {self.__vyo.FA(ctx).id}\nIA: {self.__vyo.IA(ctx).id}\nMILCOM: {self.__vyo.MILCOM(ctx).id}\nECON: {self.__vyo.ECON(ctx).id}\nECONNB: {self.__vyo.ECONNB(ctx).id}\nMEMBER: {self.__vyo.MEMBER(ctx).id}")
                            elif alliance == "varangian guard" or alliance == "vg":
                                await ctx.send(
                                    f"LEADER: {self.__vg.LEADER(ctx).id}\nHEADDEPT: {self.__vg.HEADDEPT(ctx).id}\nFA: {self.__vg.FA(ctx).id}\nIA: {self.__vg.IA(ctx).id}\nMILCOM: {self.__vg.MILCOM(ctx).id}\nECON: {self.__vg.ECON(ctx).id}\nECONNB: {self.__vg.ECONNB(ctx).id}\nMEMBER: {self.__vg.MEMBER(ctx).id}")
                elif args[0] == "register":
                    alliance = args[1]
                    target = int(args[2])
                    nation_id = int(args[3])

                    discord_user = discord.utils.get(ctx.guild.members, id=target)

                    nation = Nation(self.__kit, nation_id)
                    nation.setDiscord(discord_user)

                    if alliance.isdigit():
                        if int(alliance) == 13111:
                            self.__vyo.addMember(nation.discordId(), nation)
                            self.__vyo.save()
                        elif int(alliance) == 13173:
                            self.__vg.addMember(nation.discordId(), nation)
                            self.__vg.save()
                    else:
                        if alliance == "valyrian order" or alliance == "vyo":
                            self.__vyo.addMember(nation.discordId(), nation)
                            self.__vyo.save()
                        elif alliance == "varangian guard" or alliance == "vg":
                            self.__vg.addMember(nation.discordId(), nation)
                            self.__vg.save()

        bot.run(self.__token)