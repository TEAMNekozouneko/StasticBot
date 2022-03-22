from collections import Counter
import discord, sys
from discord.ext import commands

sys.path.append("../")
from statistic_util import dblib, log, LogLevel, config

class Dashboard(commands.Cog):
    
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self._last_member = None

        self.db = dblib.manager()
        self.cfg = config.loadConfig()
    
    @commands.slash_command(name="dashboard", description="ユーザーのダッシュボードを表示します。")
    async def cmd_dashboard(self, ctx: discord.ApplicationContext):
        await ctx.interaction.response.send_message(embed=discord.Embed(title="データベースにアクセス中...", color=discord.Color.green()), ephemeral=True)
        
        l = []
        for msg in self.db.get_contents(f"{self.cfg['database']['prefix']}message", f"author_id = {ctx.author.id}"):
            if (msg[0] == ctx.author.id):
                l = l + [msg]
        
        i = []
        for msg in self.db.get_contents(f"{self.cfg['database']['prefix']}message", f"author_id = {ctx.author.id} AND guild_id = {ctx.author.guild.id}"):
            if (msg[0] == ctx.author.id and msg[3] == ctx.guild.id):
                i = i + [msg]

        s = []
        for guild in self.db.get_contents(f"{self.cfg['database']['prefix']}message", f"author_id = {ctx.author.id}"):
            s = s + [guild[3]]

        guild_id = Counter(s).most_common()[0][0]
        guild_message_count = Counter(s).most_common()[0][1]

        g = self.bot.get_guild(guild_id)
        
        embed = discord.Embed(title="ダッシュボード", color=discord.Color.green())
        embed.add_field(name="メッセージ件数", value=f"{'{:,}'.format(len(i))}/{'{:,}'.format(len(l))}件")
        embed.add_field(name="一番メッセージを送信するサーバー", value=f"{g.name} ({'{:,}'.format(guild_message_count)})")

        await ctx.edit(embed=embed)

def setup(bot: discord.Bot):
    bot.add_cog(Dashboard(bot))