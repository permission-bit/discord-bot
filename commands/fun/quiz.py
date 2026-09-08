import discord
import random

from discord import app_commands

active_quizzes = {}


def setup(tree, db):

    cursor = db.cursor()

    @tree.command(
        name="quiz",
        description="Startet ein Quiz mit Schwierigkeitsgrad"
    )
    @app_commands.describe(
        schwierigkeitsgrad="einfach, mittel oder schwer"
    )
    async def quiz(
        interaction: discord.Interaction,
        schwierigkeitsgrad: str
    ):

        schwierigkeitsgrad = schwierigkeitsgrad.lower()

        if schwierigkeitsgrad not in questions:
            await interaction.response.send_message(
                "❌ Ungültig. Nutze: einfach, mittel oder schwer",
                ephemeral=True
            )
            return

        question = random.choice(
            questions[schwierigkeitsgrad]
        )

        active_quizzes[interaction.user.id] = {
            "question": question,
            "difficulty": schwierigkeitsgrad,
            "answers": question["answers"],
            "correct": question["correct"]
        }

        embed = discord.Embed(
            title=f"🧠 Quiz ({schwierigkeitsgrad.upper()})",
            description=question["question"],
            color=discord.Color.blue()
        )

        for i, answer in enumerate(question["answers"], 1):
            embed.add_field(
                name=f"{i}.",
                value=answer,
                inline=False
            )

        embed.set_footer(
            text="Antworte mit 1-4"
        )

        await interaction.response.send_message(embed=embed)


    @tree.command(
        name="rangliste",
        description="Zeigt die besten Quiz-Spieler"
    )
    async def leaderboard(interaction: discord.Interaction):

        cursor.execute("""
            SELECT username, points
            FROM scores
            ORDER BY points DESC
            LIMIT 10
        """)

        rows = cursor.fetchall()

        text = ""

        for i, row in enumerate(rows, 1):
            text += f"**{i}. {row[0]}** - {row[1]} Punkte\n"

        if not text:
            text = "Noch keine Spieler."

        embed = discord.Embed(
            title="🏆 Quiz Rangliste",
            description=text,
            color=discord.Color.gold()
        )

        await interaction.response.send_message(embed=embed)


# -------------------------
# Fragen
# -------------------------

questions = {
    "einfach": [
        {
            "question": "Was ist die Hauptstadt von Deutschland?",
            "answers": ["Berlin", "München", "Hamburg", "Köln"],
            "correct": "Berlin"
        },
        {
            "question": "Welche Farbe hat Gras meistens?",
            "answers": ["Blau", "Grün", "Rot", "Gelb"],
            "correct": "Grün"
        },

        {
            "question": "Was ist die Quadratwurzel aus 144?",
            "answers": ["9", "7", "17", "12"],
            "correct": "12"
        }
    ],

    "mittel": [
        {
            "question": "Wer entwickelte Linux?",
            "answers": ["Bill Gates", "Linus Torvalds", "Steve Jobs", "Elon Musk"],
            "correct": "Linus Torvalds"
        },
        {
            "question": "Wie viele Bits hat ein Byte?",
            "answers": ["4", "8", "16", "32"],
            "correct": "8"
        }
    ],

    "schwer": [
        {
            "question": "Welcher Algorithmus wird häufig für Sortierung verwendet?",
            "answers": [
                "QuickSort",
                "HTTP",
                "DNS",
                "FTP"
            ],
            "correct": "QuickSort"
        },
        {
            "question": "Was bedeutet SQL?",
            "answers": [
                "Structured Query Language",
                "Simple Queue Logic",
                "System Query Link",
                "Secure Question Layer"
            ],
            "correct": "Structured Query Language"
        },
        {
            "question": "Mit welcher Geschwindigkeit bewegt sich das Licht circa?",
            "answers": [
                "1.700m/s",
                "27.000km/h",
                "300.000m/s",
                "540km/h"
            ],
            "correct": "300.000m/s"
        },
        {
            "question": "Wie heißt der hellste mit dem Auge am Nachthimmel zu sehende Stern?",
            "answers": [
                "Malfoy",
                "Sirius",
                "Polar Stern",
                "Sagittarius A Stern"
            ],
            "correct": "Sirius"
        }       

    ]
}

