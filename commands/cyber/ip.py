import discord

from discord import app_commands
import requests
# ------------------------
# IP Informationen
# ------------------------
def ip_infos(tree):
    @tree.command(name="ip", description="IP Informationen")
    @app_commands.describe(ip="IPv4-Adresse")
    async def ip_lookup(interaction: discord.Interaction, ip: str):

        try:

            r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10)
            data = r.json()

            await interaction.response.send_message(
                f"""
    **IP**
    {data.get("ip")}

    **Ort**
    {data.get("city")}

    **Region**
    {data.get("region")}

    **Land**
    {data.get("country")}

    **Organisation**
    {data.get("org")}
    """
            )

        except Exception as e:
            await interaction.response.send_message(str(e))
