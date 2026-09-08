import discord
from discord import app_commands


def setup(tree, db):

    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS warnings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        moderator_id INTEGER,
        reason TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    db.commit()


    @tree.command(
        name="warn",
        description="Verwarnt einen Benutzer"
    )
    @app_commands.describe(
        user="Benutzer",
        reason="Grund"
    )
    async def warn(
        interaction: discord.Interaction,
        user: discord.Member,
        reason: str
    ):

        cursor.execute("""
        INSERT INTO warnings(
            user_id,
            moderator_id,
            reason
        )
        VALUES (?, ?, ?)
        """,
        (
            user.id,
            interaction.user.id,
            reason
        ))

        db.commit()


        await interaction.response.send_message(
            f"⚠️ {user.mention} wurde verwarnt.\n"
            f"Grund: {reason}"
        )