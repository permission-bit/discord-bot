import discord
from discord import app_commands
import whois

# ------------------------
# WHOIS
# ------------------------
def whoisdomain(tree):
    @tree.command(name="whois", description="WHOIS einer Domain")
    @app_commands.describe(domain="Beispiel: openai.com")
    async def whois_lookup(interaction: discord.Interaction, domain: str):

        try:
            data = whois.whois(domain)

            await interaction.response.send_message(
                f"""
    **Domain**
    {data.domain_name}

    **Registrar**
    {data.registrar}

    **Erstellt**
    {data.creation_date}

    **Läuft ab**
    {data.expiration_date}
    """
            )

        except Exception as e:
            await interaction.response.send_message(str(e))