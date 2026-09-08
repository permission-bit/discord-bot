import discord
from discord import app_commands


ROLE_MAP = {
    "🐍 Python": "Python",
    "🔐 Security": "Security",
    "💻 Developer": "Developer"
}


class RoleSelect(discord.ui.Select):

    def __init__(self):

        options = []

        for label in ROLE_MAP:
            options.append(
                discord.SelectOption(
                    label=label,
                    value=label
                )
            )


        super().__init__(
            placeholder="Wähle deine Rolle...",
            min_values=1,
            max_values=1,
            options=options
        )


    async def callback(self, interaction: discord.Interaction):

        selected = self.values[0]

        role_name = ROLE_MAP[selected]


        role = discord.utils.get(
            interaction.guild.roles,
            name=role_name
        )


        if role is None:
            await interaction.response.send_message(
                f"❌ Rolle {role_name} existiert nicht.",
                ephemeral=True
            )
            return


        member = interaction.user


        if role in member.roles:

            await member.remove_roles(role)

            await interaction.response.send_message(
                f"➖ Rolle entfernt: **{role.name}**",
                ephemeral=True
            )

        else:

            await member.add_roles(role)

            await interaction.response.send_message(
                f"✅ Rolle hinzugefügt: **{role.name}**",
                ephemeral=True
            )



class RoleView(discord.ui.View):

    def __init__(self):

        super().__init__(
            timeout=None
        )

        self.add_item(
            RoleSelect()
        )



def setup(tree):


    @tree.command(
        name="rollenmenü",
        description="Erstellt ein Rollen Auswahlmenü"
    )
    async def rollenmenu(
        interaction: discord.Interaction
    ):


        embed = discord.Embed(
            title="🎭 Rollen Auswahl",
            description=
            """
Wähle deine Interessen:

🐍 Python
🔐 Security
💻 Developer

Du kannst eine Rolle jederzeit wieder entfernen.
""",
            color=discord.Color.blue()
        )


        await interaction.response.send_message(
            embed=embed,
            view=RoleView()
        )