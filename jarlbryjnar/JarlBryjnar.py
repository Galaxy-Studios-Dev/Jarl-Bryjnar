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

from jarlbryjnar.embeds.ActivityAuditEmbed import ActivityAuditEmbed
from jarlbryjnar.embeds.AllianceEmbed import AllianceEmbed
from jarlbryjnar.embeds.ArchiveEmbed import ArchiveEmbed
from jarlbryjnar.embeds.MilcomAuditEmbed import MilcomAuditEmbed
from jarlbryjnar.embeds.InfoEmbed import InfoEmbed
from jarlbryjnar.embeds.NationEmbed import NationEmbed
from jarlbryjnar.embeds.NewMemberEmbed import NewMemberEmbed

class JarlBryjnar:
    __token = ""
    __kit = ""

    __default_path = "Discord Bots/pwbots/"

    __vyo = {}
    __vg = {}
    # __mf = {}

    def __init__(self, token):
        self.__token = token
        self.__kit = SimplePnW("f1e65cb20de0af9c1ede", self.__default_path, True)

        self.__vyo = Alliance(self.__kit, 13111)
        self.__vyo.createDirectory()

        self.__vg = Alliance(self.__kit, 13173)
        self.__vg.createDirectory()

        # self.__mf = Alliance(self.__kit, 0)
        # self.__mf.createDirectory()

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
            # self.__mf.setup()

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

            vyo_leader = self.__vyo.discordRole(interaction, "LEADER")
            vyo_headdept = self.__vyo.discordRole(interaction, "HEADDEPT")

            vg_leader = self.__vg.discordRole(interaction, "LEADER")
            vg_headdept = self.__vg.discordRole(interaction, "HEADDEPT")

            followup = interaction.followup

            if vyo_leader in roles or vyo_headdept in roles or vg_leader in roles or vg_headdept in roles:
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

                await interaction.user.add_roles(self.__vyo.discordRole(interaction, "MEMBER"))
                await interaction.response.send_message(embed=NewMemberEmbed(alliance.value, nation))
                return
            elif alliance.value == 13173 and nation.get().alliance().name == "Varangian Guard":
                self.__vg.addMember(nation.discordId(), nation)
                self.__vg.save()

                await interaction.user.add_roles(self.__vg.discordRole(interaction, "MEMBER"))
                await interaction.response.send_message(embed=NewMemberEmbed(alliance.value, nation))
                return
            elif alliance.value == 1:
                pass

        @bot.command(
            command_prefix=["!"]
        )
        async def admin(ctx, *args):
            roles = ctx.author.roles
            vyo_leader = self.__vyo.discordRole(ctx, "LEADER")
            vg_leader = self.__vg.discordRole(ctx, "LEADER")

            if vyo_leader in roles or vg_leader in roles or ctx.author.global_name == self.__vyo.discord().owner.global_name:
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
                            if bot_role in self.__vyo.discordRoles().keys():
                                previous_role_id = self.__vyo.discordRoles()[bot_role]
                                self.__vyo.setSpecificDiscordRole(bot_role, role_id)
                                self.__vyo.save()

                                await ctx.send(f"You have successfully changed {bot_role} to {role_id} [last value ~> {previous_role_id}]")
                            else:
                                await ctx.send(f"Ignoring....")
                        elif int(alliance) == 13173 or alliance == "varangian guard" or alliance == "vg":
                            if bot_role in self.__vg.discordRoles().keys():
                                previous_role_id = self.__vg.discordRoles()[bot_role]
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
                                leader = self.__vyo.discordRole(ctx, "LEADER").id
                                head_dept = self.__vyo.discordRole(ctx, "HEADDEPT").id
                                fa = self.__vyo.discordRole(ctx, "FA").id
                                ia = self.__vyo.discordRole(ctx, "IA").id
                                milcom = self.__vyo.discordRole(ctx, "MILCOM").id
                                econ = self.__vyo.discordRole(ctx, "ECON").id
                                econnb = self.__vyo.discordRole(ctx, "ECONNB").id
                                member = self.__vyo.discordRole(ctx, "MEMBER").id

                                await ctx.send(f"LEADER: {leader}\nHEADDEPT: {head_dept}\nFA: {fa}\nIA: {ia}\nMILCOM: {milcom}\nECON: {econ}\nECONNB: {econnb}\nMEMBER: {member}")
                            elif int(alliance) == 13173:
                                leader = self.__vg.discordRole(ctx, "LEADER").id
                                head_dept = self.__vg.discordRole(ctx, "HEADDEPT").id
                                fa = self.__vg.discordRole(ctx, "FA").id
                                ia = self.__vg.discordRole(ctx, "IA").id
                                milcom = self.__vg.discordRole(ctx, "MILCOM").id
                                econ = self.__vg.discordRole(ctx, "ECON").id
                                econnb = self.__vg.discordRole(ctx, "ECONNB").id
                                member = self.__vg.discordRole(ctx, "MEMBER").id

                                await ctx.send(f"LEADER: {leader}\nHEADDEPT: {head_dept}\nFA: {fa}\nIA: {ia}\nMILCOM: {milcom}\nECON: {econ}\nECONNB: {econnb}\nMEMBER: {member}")
                        else:
                            if alliance == "valyrian order" or alliance == "vyo":
                                leader = self.__vyo.discordRole(ctx, "LEADER").id
                                head_dept = self.__vyo.discordRole(ctx, "HEADDEPT").id
                                fa = self.__vyo.discordRole(ctx, "FA").id
                                ia = self.__vyo.discordRole(ctx, "IA").id
                                milcom = self.__vyo.discordRole(ctx, "MILCOM").id
                                econ = self.__vyo.discordRole(ctx, "ECON").id
                                econnb = self.__vyo.discordRole(ctx, "ECONNB").id
                                member = self.__vyo.discordRole(ctx, "MEMBER").id

                                await ctx.send(f"LEADER: {leader}\nHEADDEPT: {head_dept}\nFA: {fa}\nIA: {ia}\nMILCOM: {milcom}\nECON: {econ}\nECONNB: {econnb}\nMEMBER: {member}")
                            elif alliance == "varangian guard" or alliance == "vg":
                                leader = self.__vg.discordRole(ctx, "LEADER").id
                                head_dept = self.__vg.discordRole(ctx, "HEADDEPT").id
                                fa = self.__vg.discordRole(ctx, "FA").id
                                ia = self.__vg.discordRole(ctx, "IA").id
                                milcom = self.__vg.discordRole(ctx, "MILCOM").id
                                econ = self.__vg.discordRole(ctx, "ECON").id
                                econnb = self.__vg.discordRole(ctx, "ECONNB").id
                                member = self.__vg.discordRole(ctx, "MEMBER").id

                                await ctx.send(f"LEADER: {leader}\nHEADDEPT: {head_dept}\nFA: {fa}\nIA: {ia}\nMILCOM: {milcom}\nECON: {econ}\nECONNB: {econnb}\nMEMBER: {member}")
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

                            await ctx.send(embed=NewMemberEmbed(alliance, nation))
                        elif int(alliance) == 13173:
                            self.__vg.addMember(nation.discordId(), nation)
                            self.__vg.save()

                            await ctx.send(embed=NewMemberEmbed(alliance, nation))
                    else:
                        if alliance == "valyrian order" or alliance == "vyo":
                            self.__vyo.addMember(nation.discordId(), nation)
                            self.__vyo.save()

                            await ctx.send(embed=NewMemberEmbed(alliance, nation))
                        elif alliance == "varangian guard" or alliance == "vg":
                            self.__vg.addMember(nation.discordId(), nation)
                            self.__vg.save()

                            await ctx.send(embed=NewMemberEmbed(alliance, nation))

        bot.run(self.__token)