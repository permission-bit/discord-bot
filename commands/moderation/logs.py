import discord


def setup(tree):


    @tree.command(
        name="userinfo",
        description="Zeigt Benutzerinformationen"
    )
    async def userinfo(
        interaction: discord.Interaction,
        user: discord.Member = None
    ):

        if user is None:
            user = interaction.user


        embed = discord.Embed(
            title="👤 Benutzerinfo",
            color=discord.Color.blue()
        )


        embed.add_field(
            name="Name",
            value=user.name
        )


        embed.add_field(
            name="ID",
            value=user.id
        )


        embed.add_field(
            name="Beigetreten",
            value=user.joined_at.strftime("%d.%m.%Y")
        )


        embed.set_thumbnail(
            url=user.display_avatar.url
        )


        await interaction.response.send_message(
            embed=embed
        )