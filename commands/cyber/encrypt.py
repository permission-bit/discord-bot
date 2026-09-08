import discord
from discord import app_commands
import hashlib

# ------------------------
# SHA256 / MD5
# ------------------------
def algorithm(tree, db):
    @tree.command(name="hash", description="Berechnet Hashes")
    @app_commands.describe(text="Zu hashender Text")
    async def hash_cmd(interaction: discord.Interaction, text: str):

        md5 = hashlib.md5(text.encode()).hexdigest()
        sha1 = hashlib.sha1(text.encode()).hexdigest()
        sha256 = hashlib.sha256(text.encode()).hexdigest()

        await interaction.response.send_message(
            f"""
    **MD5**
    `{md5}`

    **SHA1**
    `{sha1}`

    **SHA256**
    `{sha256}`
    """
        )