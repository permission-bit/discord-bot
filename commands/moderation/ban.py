import discord
from discord import app_commands
from config import PROTECTED_USERS


def setup(tree):


    @tree.command(
        name="ban",
        description="Bannt einen Benutzer"
    )
    @app_commands.describe(
        user="Benutzer",
        reason="Grund"
    )
    async def ban(
        interaction: discord.Interaction,
        user: discord.Member,
        reason: str = "Kein Grund angegeben"
    ):

        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message(
                "❌ Keine Berechtigung.",
                ephemeral=True
            )
            return


        # Geschützte Benutzer prüfen
        if user.id in PROTECTED_USERS:
            await interaction.response.send_message(
                "🛡️ Dieser Benutzer ist geschützt und kann nicht gebannt werden.",
                ephemeral=True
            )
            return


        await user.ban(
            reason=reason
        )


        await interaction.response.send_message(
            f"🔨 {user.mention} wurde gebannt.\n"
            f"Grund: {reason}"
        )