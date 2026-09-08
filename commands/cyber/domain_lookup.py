import discord
from discord import app_commands
import dns

# ------------------------
# DNS Lookup
# ------------------------
def lookup(tree):
    @tree.command(name="dns", description="DNS A-Records")
    @app_commands.describe(domain="Beispiel: openai.com")
    async def dns_lookup(interaction: discord.Interaction, domain: str):

        try:
            result = dns.resolver.resolve(domain, "A")

            ips = "\n".join(str(r) for r in result)

            await interaction.response.send_message(
                f"**{domain}**\n```{ips}```"
            )

        except Exception as e:
            await interaction.response.send_message(str(e))