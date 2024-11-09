import requests
from discord.ext import commands
import discord


class IPLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def iplookup(self, ctx, ip: str):
        try:
            # URLを構築
            url = f"https://ipapi.co/{ip}/json/"
            print(url)
            # IP情報を取得
            response = requests.get(url)
            data = response.json()
            
            if response.status_code != 200:
                await ctx.send(f"Error fetching details for IP address {ip}: {data.get('error', 'Unknown error')}")
                return

            # Embedメッセージの作成
            embed = discord.Embed(title="IP Lookup Results", color=discord.Color.blue())
            embed.add_field(name="IP Address", value=data.get('ip', 'N/A'), inline=False)
            embed.add_field(name="Country", value=data.get('country_name', 'N/A'), inline=False)
            embed.add_field(name="Region", value=data.get('region', 'N/A'), inline=False)
            embed.add_field(name="City", value=data.get('city', 'N/A'), inline=False)
            embed.add_field(name="Time Zone", value=data.get('timezone', 'N/A'), inline=False)
            embed.add_field(name="ISP", value=data.get('org', 'N/A'), inline=False)
            embed.add_field(name="Languages", value=data.get('languages', 'N/A'), inline=False)
            embed.add_field(name="ASN", value=f"ASN: {data.get('asn', 'N/A')}\n"
                                              f"Organization: {data.get('org', 'N/A')}", inline=False)
            embed.set_footer(text="Powered by ipapi")

            await ctx.send(embed=embed)
            print(f"IP Lookup Running: {data['ip']}")
        except Exception as e:
            await ctx.send(f"Error fetching details for IP address {ip}: {e}")
async def setup(bot):
    await bot.add_cog(IPLookup(bot))
