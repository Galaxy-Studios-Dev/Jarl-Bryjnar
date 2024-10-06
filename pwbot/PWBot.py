import os.path

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from simplepnw.SimplePnW import SimplePnW
from simplepnw.queries.Nation import Nation

from pwbot.alliances.ValyrianOrder import ValyrianOrder
from pwbot.alliances.VarangianGuard import VarangianGuard
from pwbot.embeds.AllianceEmbed import AllianceEmbed
from pwbot.embeds.ArchiveEmbed import ArchiveEmbed
from pwbot.embeds.AuditEmbed import AuditEmbed
from pwbot.embeds.BaseballTeamPlayersEmbed import BaseballTeamPlayersEmbed
from pwbot.embeds.BaseballTeamStatsEmbed import BaseballTeamStatsEmbed
from pwbot.embeds.InfoEmbed import InfoEmbed
from pwbot.embeds.NationEmbed import NationEmbed
from pwbot.embeds.NewMemberEmbed import NewMemberEmbed
from pwbot.utils.FileManager import FileManager
from pwbot.utils.Formatter import Formatter
from pwbot.utils.Math import Math
from pwbot.utils.RoleIds import RoleIds

file_manager = FileManager()
formatter = Formatter()

role_ids = RoleIds()

class PWBot:
    __token = ""
    __kit = ""

    __vyo = {}
    __vg = {}

    def __init__(self, token):
        self.__token = token
        self.__kit = SimplePnW("f1e65cb20de0af9c1ede")

    def run(self):

        bot = commands.Bot(command_prefix=['$', '!'], intents=discord.Intents.all())

        @bot.event
        async def on_ready():
            self.__vyo = ValyrianOrder(self.__kit)
            self.__vg = VarangianGuard(self.__kit)

            try:
                synced = await bot.tree.sync()
                print(f"Synced {len(synced)} command(s)")
            except Exception as e:
                print(e)

        @bot.tree.command(name="archive")
        @app_commands.describe(alliance="which alliance to access")
        @app_commands.choices(alliance=[
                app_commands.Choice(name="Valyrian Order", value=13111),
                app_commands.Choice(name="Varangian Guard", value=13173)
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
                app_commands.Choice(name="Build", value="builds")
            ],
                alliance=[
                app_commands.Choice(name="Valyrian Order", value=13111),
                app_commands.Choice(name="Varangian Guard", value=13173)
            ]
        )
        async def audit(interaction: discord.Interaction, audit_type: app_commands.Choice[str], alliance: app_commands.Choice[int]):
            roles = interaction.user.roles

            followup = interaction.followup

            if self.__vyo.LEADER(interaction) in roles or self.__vyo.MILCOM(interaction) in roles or self.__vg.LEADER(interaction) in roles or self.__vg.MILCOM(interaction) in roles:
                if audit_type.value == "milcom":
                    if alliance.value == 13111:
                        if interaction.guild.id == 1278478363400339481:
                            webhook_url = self.__vyo.getWebhookUrl('audit') # "https://discord.com/api/webhooks/1291106096668479620/GwIYLxAqlIuU5Y1EZvm0w4lSU1UumE6YqsMsKATLBRbWSV4rTxOQzpLST8ptotSnPcz2"
                        elif interaction.guild.id == 1283514897224958003:
                            webhook_url = self.__vyo.getWebhookUrl('audit') # "https://discord.com/api/webhooks/1291106096668479620/GwIYLxAqlIuU5Y1EZvm0w4lSU1UumE6YqsMsKATLBRbWSV4rTxOQzpLST8ptotSnPcz2"

                        members = self.__vyo.getMembers()

                        for member in members:
                            member = members[member]

                            if len(member.getCities()) >= 16:
                                mmr_key = 'production'
                                required_mmr = self.__vyo.getMMR(mmr_key)
                                member.setDiscordUser(interaction.user)

                                embed = member.checkMMR(AuditEmbed(alliance.value, member, self.__vyo.formatMMR(mmr_key)), required_mmr)

                            elif len(member.getCities()) < 16:
                                mmr_key = 'raider'
                                required_mmr = self.__vyo.getMMR(mmr_key)
                                member.setDiscordUser(interaction.user)

                                embed = member.checkMMR(AuditEmbed(alliance.value, member, self.__vyo.formatMMR(mmr_key)), required_mmr)


                            async with aiohttp.ClientSession() as session:
                                webhook = followup.from_url(webhook_url, session=session)
                                await webhook.send(embed=embed, username='Jarl Bryjnar')
                    elif alliance.value == 13173:
                        if interaction.guild.id == 1278478363400339481:
                            webhook_url = self.__vg.getWebhookUrl('audit') # "https://discord.com/api/webhooks/1291118659074265220/pUHVxYeS8LAnQ7jvmah0M59xZjmAMupXAJKciLp0F3a33V3QoRSRYxlU9u9cjEYgjH-q"
                        elif interaction.guild.id == 1283514897224958003:
                            webhook_url = self.__vg.getWebhookUrl('audit') # "https://discord.com/api/webhooks/1291118659074265220/pUHVxYeS8LAnQ7jvmah0M59xZjmAMupXAJKciLp0F3a33V3QoRSRYxlU9u9cjEYgjH-q"

                        members = self.__vg.getMembers()

                        for member in members:
                            member = members[member]

                            if len(member.getCities()) >= 16:
                                mmr_key = "production"
                                required_mmr = self.__vg.getMMR(mmr_key)
                                member.setDiscordUser(interaction.user)

                                embed = member.checkMMR(AuditEmbed(alliance.value, member, self.__vg.formatMMR(mmr_key)), required_mmr)
                            elif len(member.getCities()) < 16:
                                mmr_key = "raider"
                                required_mmr = self.__vg.getMMR(mmr_key)
                                member.setDiscordUser(interaction.user)

                                embed = member.checkMMR(AuditEmbed(alliance.value, member, self.__vg.formatMMR(mmr_key)), required_mmr)

                            async with aiohttp.ClientSession() as session:
                                webhook = followup.from_url(webhook_url, session=session)
                                await webhook.send(embed=embed, username='Jarl Bryjnar')
            elif self.__vyo.LEADER() in roles or self.__vyo.IA() or self.__vg.LEADER() in roles or self.__vg.IA() in roles:
                if audit_type.value == "build":
                    if alliance.value == 13111:
                        await interaction.response.send_message(f"Starting build audit on Valyrian Order...")
                    elif alliance.name == 13173:
                        await interaction.response.send_message(f"Starting build audit on Varangian Guard...")

        @bot.tree.command(name="baseball")
        @app_commands.describe(decision="what would you like to do")
        @app_commands.choices(decision=[
                app_commands.Choice(name="Stats", value="stats"),
                app_commands.Choice(name="Players", value="players")
            ]
        )
        async def baseball(interaction: discord.Interaction, decision: app_commands.Choice[str]):
            discord_id = str(interaction.user.id)

            if decision.value == "stats":
                if discord_id in self.__vyo.getMembers().keys():
                    member = self.__vyo.getMembers()[discord_id]
                    query = self.__kit.query('nation', member.getId())

                    team = query.getBaseballTeam()
                    embed = BaseballTeamStatsEmbed(team)
                    await interaction.response.send_message(embed=embed)
                elif discord_id in self.__vg.getMembers().keys():
                    member = self.__vg.getMembers()[discord_id]
                    query = self.__kit.query('nation', member.getId())
                    team = query.getBaseballTeam()

                    embed = BaseballTeamStatsEmbed(team)
                    await interaction.response.send_message(embed=embed)
            elif decision.value == "players":
                discord_id = str(interaction.user.id)

                if discord_id in self.__vyo.getMembers().keys():
                    member = self.__vyo.getMembers()[discord_id]
                    query = self.__kit.query('nation', member.getId())
                    team = query.getBaseballTeam()

                    embed = BaseballTeamPlayersEmbed(team)
                    await interaction.response.send_message(embed=embed)
                elif discord_id in self.__vg.getMembers().keys():
                    member = self.__vg.getMembers()[discord_id]
                    query = self.__kit.query('nation', member.getId())
                    team = query.getBaseballTeam()

                    embed = BaseballTeamPlayersEmbed(team)
                    await interaction.response.send_message(embed=embed)

        @bot.tree.command(name="info")
        async def info(interaction: discord.Interaction):
            bigt = discord.utils.get(interaction.guild.members, id=1177716521573818398)
            embed = InfoEmbed(bigt.avatar.url)
            await interaction.response.send_message(embed=embed)

        @bot.tree.command(name="register")
        @app_commands.describe(alliance="The alliance you are in", nation_id="Id of nation to register")
        @app_commands.choices(alliance=[
            app_commands.Choice(name="Valyrian Order", value="vyo"),
            app_commands.Choice(name="Varangian Guard", value="vg"),
            app_commands.Choice(name="ADMIN", value='admin')
        ])
        async def register(interaction: discord.Interaction, alliance: app_commands.Choice[str], nation_id: int):
            discord_id = str(interaction.user.id)
            query = self.__kit.query('nation', nation_id)

            if alliance.value == "vyo" and query.getAlliance().name == "Valyrian Order":
                direct_path = f"{alliance.value}/{discord_id}"

                if os.path.exists(f"{file_manager.members_path}{direct_path}.json"):
                    await interaction.response.send_message(formatter.alreadyRegistered())
                else:
                    embed = NewMemberEmbed(alliance.value, query)
                    self.__vyo.getMembers()[discord_id] = file_manager.createMemberFile(self.__kit, direct_path, {'discord': interaction.user, 'nation_id': nation_id})

                    await interaction.response.send_message(embed=embed)
            elif alliance.value == "vg" and query.getAlliance().name == "Varangian Guard":
                direct_path = f"{alliance.value}/{discord_id}"

                if os.path.exists(f"{file_manager.members_path}{direct_path}.json"):
                    await interaction.response.send_message(formatter.alreadyRegistered())
                else:
                    embed = NewMemberEmbed(alliance.value, query)
                    self.__vg.getMembers()[str(discord_id)] = file_manager.createMemberFile(self.__kit, direct_path, {'discord': interaction.user, 'nation_id': nation_id})

                    await interaction.response.send_message(embed=embed)

        @bot.tree.command(name="transfer")
        @app_commands.describe()
        async def transfer(interaction: discord.Interaction):
            pass

        @bot.tree.command(name="treasury")
        @app_commands.describe(transaction="what kind of transaction it is", coal="amount of coal", iron="amount of iron", lead="amount of lead", bauxite="amount of bauxite",
                               oil="amount of oil", uranium="amount of uranium", food="amount of food", steel="amount of steel", aluminum="amount of aluminum",
                               gasoline="amount of gasoline", munitions="amount of munitions", money="amount of money")
        @app_commands.choices(transaction=[
                app_commands.Choice(name="Withdraw", value="withdraw"),
                app_commands.Choice(name="Deposit", value="deposit")
            ]
        )
        async def treasury(interaction: discord.Interaction, transaction: app_commands.Choice[str], coal: int, iron: int, lead: int, bauxite: int, oil: int, uranium: int, food: int, steel: int, aluminum: int, gasoline: int, munitions: int, money: int):
            roles = interaction.user.roles
            SELF_WITHDRAW = True

            if self.__vyo.MEMBER(interaction) in roles and SELF_WITHDRAW or self.__vg.MEMBER(interaction) in roles and SELF_WITHDRAW:
                if transaction.value == "withdraw":
                    print(f"Starting withdraw process of:\n{coal} Coal\n{iron} Iron\n{lead} Lead\n{bauxite} Bauxite\n{oil} Oil\n{uranium} Uranium\n{food} Food\n{steel} Steel\n{aluminum} Aluminum\n{gasoline} Gasoline\n{munitions} Munitions\n${money}")
                elif transaction.value == "deposit":
                    print(f"Starting deposit process of:\n{coal} Coal\n{iron} Iron\n{lead} Lead\n{bauxite} Bauxite\n{oil} Oil\n{uranium} Uranium\n{food} Food\n{steel} Steel\n{aluminum} Aluminum\n{gasoline} Gasoline\n{munitions} Munitions\n${money}")

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
                print("Querrying P&W Api...")
                query = self.__kit.query('alliance', given_id)
                print("Creating new alliance embed....")
                embed = AllianceEmbed(query)
                await interaction.followup.send(embed=embed)
                print(f"Response: Pass\nTime: {int(round(bot.latency * 1000))} ms")
            elif alliance.value == 0:
                await interaction.response.defer()

                query = self.__kit.query('nation', given_id)
                embed = NationEmbed(query)
                await interaction.followup.send(embed=embed)

        @bot.command(
            command_prefix=["!"]
        )
        async def admin(ctx, *args):
            roles = ctx.author.roles

            if self.__vyo.LEADER(ctx) in roles or self.__vyo.HEADDEPT(ctx) in roles or self.__vg.LEADER(ctx) in roles or self.__vg.HEADDEPT(ctx) in roles:
                if args[0] == "register":
                    alliance = args[1]
                    nation_id = int(args[2])
                    discord_user = discord.utils.get(ctx.guild.members, id=int(args[3]))
                    query = self.__kit.query('nation', nation_id)

                    if alliance == "vyo" or alliance == 13111:
                        direct_path = f"vyo/{args[3]}"

                        if os.path.exists(f"{file_manager.members_path}{direct_path}.json"):
                            await ctx.send(formatter.alreadyRegisteredAdmin(discord_user))
                        else:
                            embed = NewMemberEmbed("vyo", query)
                            self.__vyo.getMembers()[discord_user.id] = file_manager.createMemberFile(self.__kit, direct_path, {'discord': discord_user, 'nation_id': nation_id})

                            await ctx.send(embed=embed)
                    elif alliance == "vg" or alliance == 13173:
                        direct_path = f"vg/{discord_user.id}"

                        if os.path.exists(f"{file_manager.members_path}{direct_path}.json"):
                            await ctx.send(formatter.alreadyRegisteredAdmin(discord_user))
                        else:
                            embed = NewMemberEmbed("vg", query)
                            self.__vg.getMembers()[discord_user.id] = file_manager.createMemberFile(self.__kit, direct_path, {'discord': discord_user, 'nation_id': nation_id})
                            await ctx.send(embed=embed)
                elif args[0] == "treasury":
                    if args[1] == "account":
                        if args[2] == "delete":
                            pass
                        elif args[2] == "reset":
                            pass

        bot.run(self.__token)