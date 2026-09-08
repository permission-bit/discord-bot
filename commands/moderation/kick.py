import discord
from discord import app_commands
from config import PROTECTED_USERS


def setup(tree):


    @tree.command(
        name="kick",
        description="Entfernt einen Benutzer"
    )
    @app_commands.describe(
        user="Benutzer",
        reason="Grund"
    )
    async def kick(
        interaction: discord.Interaction,
        user: discord.Member,
        reason: str = "Kein Grund angegeben"
    ):

        if not interaction.user.guild_permissions.kick_members:

            await interaction.response.send_message(
                "❌ Keine Berechtigung.",
                ephemeral=True
            )

            return

        if user.id in PROTECTED_USERS:
            await interaction.response.send_message(
                "🛡️ Dieser Benutzer ist geschützt.",
                ephemeral=True
            )
            return

        await user.kick(
            reason=reason
        )


        await interaction.response.send_message(
            f"👢 {user.mention} wurde gekickt.\n"
            f"Grund: {reason}"
        )