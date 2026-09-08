import random
from datetime import datetime

async def handle_message(message, quiz, cursor, db):

    if message.author.bot:
        return

    text = message.content.lower()


    # -----------------
    # Quiz Antworten
    # -----------------

    if message.author.id in quiz.active_quizzes:

        current_quiz = quiz.active_quizzes[message.author.id]

        try:
            choice = int(message.content)
            answer = current_quiz["answers"][choice - 1]

        except (ValueError, IndexError):
            return


        if answer == current_quiz["correct"]:

            difficulty = current_quiz["difficulty"]

            points = {
                "einfach": 5,
                "mittel": 10,
                "schwer": 20
            }[difficulty]


            cursor.execute("""
                INSERT INTO scores(user_id, username, points)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id)
                DO UPDATE SET points = points + ?
            """,
            (
                message.author.id,
                message.author.name,
                points,
                points
            ))

            db.commit()


            cursor.execute(
                "SELECT points FROM scores WHERE user_id=?",
                (message.author.id,)
            )

            total = cursor.fetchone()[0]


            await message.channel.send(
                f"✅ Richtig {message.author.mention}!\n"
                f"🏆 +{points} Punkte\n"
                f"💰 Gesamt: **{total} Punkte**"
            )

        else:

            await message.channel.send(
                f"❌ Falsch!\n"
                f"✅ Antwort: **{current_quiz['correct']}**"
            )


        del quiz.active_quizzes[message.author.id]

        return


    # -----------------
    # Normale Commands
    # -----------------

    if text == "!ping":

        await message.channel.send(
            "🏓 Pong!"
        )


    elif text == "!hilfe":

        await message.channel.send(
    """
📚 **Verfügbare Befehle**

**Allgemein**
`!ping` → Bot testen
`!hilfe` → Diese Übersicht
`!info` → Benutzerinformationen

**Server**
`!server` → Serverinformationen

**Spaß**
`!würfel` → Würfelt eine Zahl
`!zeit` → Aktuelle Uhrzeit

**Security**
`/hash` → Hash erzeugen
`/dns` → DNS Lookup
`/whois` → Domain Informationen
`/ip` → IP Informationen
`/resolve` → Hostname auflösen

**Quiz**
`/quiz` → Quiz starten
`/rangliste` → Bestenliste

**Moderation**
`/addrole user rolle`
→ Gibt einem Benutzer eine Rolle

`/removerole user rolle`
→ Entfernt eine Rolle von einem Benutzer

**Reaktionsrollen**
`/reactionrole`
→ Erstellt ein Rollen-Auswahlmenü

⚠️ Rollen können nur vergeben werden, wenn:
- Der Benutzer die Berechtigung "Rollen verwalten" besitzt
- Die Bot-Rolle über der Zielrolle steht
"""
    )


    elif text == "!info":

        user = message.author

        await message.channel.send(
            f"""
👤 Benutzer: {user}
🆔 ID: {user.id}
📅 Konto erstellt: {user.created_at.strftime('%d.%m.%Y')}
"""
        )


    elif text == "!server":

        guild = message.guild

        await message.channel.send(
            f"""
🏠 Server: {guild.name}
👥 Mitglieder: {guild.member_count}
📅 Erstellt: {guild.created_at.strftime('%d.%m.%Y')}
"""
        )


    elif text == "!würfel":

        zahl = random.randint(1,6)

        await message.channel.send(
            f"🎲 {zahl}"
        )


    elif text == "!zeit":

        jetzt = datetime.now().strftime("%H:%M:%S")

        await message.channel.send(
            f"🕒 {jetzt}"
        )


    elif "hallo" in text:

        await message.channel.send(
            f"Hallo {message.author.mention} 👋"
        )


    elif "python" in text:

        await message.channel.send(
            "🐍 Python ist eine tolle Sprache!"
        )


    elif "discord" in text:

        await message.add_reaction("❤️")