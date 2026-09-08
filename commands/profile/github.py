import discord
from discord import app_commands


def setup(tree, db):

    cursor = db.cursor()

    @tree.command(
        name="github",
        description="Verknüpft dein GitHub Profil"
    )
    @app_commands.describe(
        link="Dein GitHub Profil Link"
    )
    async def github(
        interaction: discord.Interaction,
        link: str
    ):

        if "github.com/" not in link:
            await interaction.response.send_message(
                "❌ Bitte einen gültigen GitHub-Link angeben.",
                ephemeral=True
            )
            return


        cursor.execute("""
        INSERT INTO profiles(user_id, github)
        VALUES (?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET github=?
        """,
        (
            interaction.user.id,
            link,
            link
        ))

        db.commit()


        await interaction.response.send_message(
            f"✅ GitHub Profil gespeichert:\n{link}",
            ephemeral=True
        )



    @tree.command(
        name="profil",
        description="Zeigt dein Profil"
    )
    async def profil(
        interaction: discord.Interaction
    ):

        cursor.execute(
            "SELECT github FROM profiles WHERE user_id=?",
            (interaction.user.id,)
        )

        result = cursor.fetchone()


        embed = discord.Embed(
            title=f"👤 Profil von {interaction.user}",
            color=discord.Color.blurple()
        )


        if result and result[0]:
            embed.add_field(
                name="🐙 GitHub",
                value=result[0],
                inline=False
            )

        else:
            embed.add_field(
                name="GitHub",
                value="Nicht hinterlegt",
                inline=False
            )


        await interaction.response.send_message(
            embed=embed
        )