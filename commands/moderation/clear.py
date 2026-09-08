import discord
from discord import app_commands


def setup(tree):

    @tree.command(
        name="clear",
        description="Löscht Nachrichten"
    )
    @app_commands.describe(
        amount="Anzahl Nachrichten"
    )
    async def clear(
        interaction: discord.Interaction,
        amount: int
    ):

        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "❌ Keine Berechtigung.",
                ephemeral=True
            )
            return


        if amount < 1 or amount > 100:
            await interaction.response.send_message(
                "❌ Bitte eine Zahl zwischen 1 und 100 eingeben.",
                ephemeral=True
            )
            return


        await interaction.response.defer(ephemeral=True)


        deleted = await interaction.channel.purge(
            limit=amount
        )


        await interaction.followup.send(
            f"🧹 {len(deleted)} Nachrichten gelöscht.",
            ephemeral=True
        )