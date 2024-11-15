import discord

class ActivityAuditEmbed(discord.Embed):
    def __init__(self, server, member, last_active, days_inactive):
        super().__init__()
        color_block = member.get().colorBlock()

        if server == 13111:
            if days_inactive > 2:
                discord_user = member.getDiscord()
                self.title = f"{member.get().name()} ({days_inactive} Days)"
                self.description = discord_user.mention + f"\n{last_active.month}/{last_active.day}/{last_active.year}"
                self.set_thumbnail(url=member.get().flag())
                self.add_field(name="", value=f"\n{discord_user.display_name}, your people miss you, Check in on them atleast 5 minutes a day!")
            else:
                discord_user = member.discord()
                self.title = f"{member.get().name()} ({days_inactive} Days)"
                self.set_thumbnail(url=member.get().flag())
                self.add_field(name="", value=f"\n{discord_user.display_name}, your people are pleased to see your frequent presence, Keep up the great work!")
        elif server == 13173:
            if days_inactive > 2:
                discord_user = member.discord()
                self.title = f"{member.get().name()} ({days_inactive} Days)"
                self.description = discord_user.mention + f"\n{last_active.month}/{last_active.day}/{last_active.year}"
                self.set_thumbnail(url=member.get().flag())
                self.add_field(name="", value=f"{discord_user.display_name}, your people miss you, Check in on them atleast 5 minutes a day!")
            else:
                discord_user = member.discord()
                self.title = f"{member.get().name()} ({days_inactive} Days)"
                self.set_thumbnail(url=member.get().flag())
                self.add_field(name="", value=f"\n{discord_user.display_name}, your people are pleased to see your frequent presence, Keep up the great work!")

        if color_block == "gray":
            self.color = discord.Color.dark_gray()
            self.add_field(name="", value=f"Your current color block is {color_block}, Please switch to the black color block!", inline=False)
        elif color_block == "black":
            pass
        elif color_block == "green":
            self.color = discord.Color.dark_green()
            self.add_field(name="", value=f"Your current color block is {color_block}, Please switch to the black color block!", inline=False)