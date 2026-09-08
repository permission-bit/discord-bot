import discord
import socket

from discord import app_commands


def setup(tree):

    @tree.command(
        name="resolve",
        description="Hostname auflösen"
    )
    @app_commands.describe(
        host="Hostname"
    )
    async def resolve(
        interaction: discord.Interaction,
        host: str
    ):

        try:
            ip = socket.gethostbyname(host)

            await interaction.response.send_message(
                f"{host} → `{ip}`"
            )

        except Exception as e:
            await interaction.response.send_message(
                f"❌ Fehler: {e}"
            )