import discord
from discord import app_commands


def setup(tree):

    @tree.command(
        name="addrole",
        description="Gibt einem Benutzer eine Rolle"
    )
    @app_commands.describe(
        user="Benutzer, der die Rolle bekommen soll",
        rolle="Name der Rolle"
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def addrole(
        interaction: discord.Interaction,
        user: discord.Member,
        rolle: str
    ):

        guild = interaction.guild

        if guild is None:
            await interaction.response.send_message(
                "❌ Nur auf Servern verfügbar.",
                ephemeral=True
            )
            return


        role = discord.utils.get(
            guild.roles,
            name=rolle
        )


        if role is None:
            await interaction.response.send_message(
                "❌ Rolle nicht gefunden.",
                ephemeral=True
            )
            return


        # Bot darf nur Rollen unter seiner eigenen Rolle vergeben
        if role >= guild.me.top_role:
            await interaction.response.send_message(
                "❌ Ich kann diese Rolle nicht vergeben. "
                "Meine Bot-Rolle muss höher stehen.",
                ephemeral=True
            )
            return


        if role in user.roles:
            await interaction.response.send_message(
                f"ℹ️ {user.mention} hat diese Rolle bereits.",
                ephemeral=True
            )
            return


        await user.add_roles(role)


        await interaction.response.send_message(
            f"✅ {user.mention} hat die Rolle **{role.name}** bekommen."
        )


    @addrole.error
    async def addrole_error(
        interaction: discord.Interaction,
        error
    ):

        if isinstance(
            error,
            app_commands.errors.MissingPermissions
        ):

            await interaction.response.send_message(
                "❌ Du brauchst die Berechtigung **Rollen verwalten**.",
                ephemeral=True
            )

    @tree.command(
        name="removerole",
        description="Entfernt eine Rolle von einem Benutzer"
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def removerole(
        interaction: discord.Interaction,
        user: discord.Member,
        rolle: str
    ):

        guild = interaction.guild

        role = discord.utils.get(
            guild.roles,
            name=rolle
        )

        if role is None:
            await interaction.response.send_message(
                "❌ Rolle nicht gefunden.",
                ephemeral=True
            )
            return


        await user.remove_roles(role)


        await interaction.response.send_message(
            f"✅ Rolle **{role.name}** wurde von {user.mention} entfernt."
        )