import discord 

def setup(tree, db):
    @tree.command(
        name="stats",
        description="Zeigt Serverstatistiken"
    )
    async def stats(interaction: discord.Interaction):

        if interaction.guild is None:
            await interaction.response.send_message(
                "❌ Dieser Befehl funktioniert nur auf Servern.",
                ephemeral=True
            )
            return

        guild = interaction.guild

        humans = sum(not member.bot for member in guild.members)
        bots = sum(member.bot for member in guild.members)

        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)

        online = sum(
            member.status != discord.Status.offline
            for member in guild.members
        )

        boost_level = guild.premium_tier
        boosts = guild.premium_subscription_count

        embed = discord.Embed(
            title=f"📊 Statistiken von {guild.name}",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="👥 Mitglieder",
            value=str(guild.member_count),
            inline=True
        )

        embed.add_field(
            name="🟢 Online",
            value=str(online),
            inline=True
        )

        embed.add_field(
            name="🤖 Bots",
            value=str(bots),
            inline=True
        )

        embed.add_field(
            name="👤 Menschen",
            value=str(humans),
            inline=True
        )

        embed.add_field(
            name="💬 Textkanäle",
            value=str(text_channels),
            inline=True
        )

        embed.add_field(
            name="🔊 Sprachkanäle",
            value=str(voice_channels),
            inline=True
        )

        embed.add_field(
            name="📁 Kategorien",
            value=str(categories),
            inline=True
        )

        embed.add_field(
            name="🚀 Boost-Level",
            value=f"Level {boost_level}",
            inline=True
        )

        embed.add_field(
            name="💎 Server-Boosts",
            value=str(boosts),
            inline=True
        )

        embed.set_footer(
            text=f"Server erstellt am {guild.created_at.strftime('%d.%m.%Y')}"
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        await interaction.response.send_message(embed=embed)
