import random
from datetime import datetime
import hashlib

import socket
from discord import app_commands

import dns.resolver
import requests
import whois

import discord
import sqlite3

import os
from dotenv import load_dotenv
from commands import moderation #Ordner
from commands.fun import quiz
from commands.server import stats

from commands.cyber import encrypt
from commands.cyber import resolve
from commands.cyber import ip
from commands.cyber import domain
from commands.cyber import domain_lookup

#----rollen
from commands.moderation import roles
from commands.moderation import reaction_roles

from commands.events import messages as message_handler

from commands.cyber import portscan

from commands.profile import github

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Für Begrüßung neuer Mitglieder

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# -------------------------
# Datenbank
# -------------------------
db = sqlite3.connect("bot.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    points INTEGER DEFAULT 0
)
""")


# Neue Profile-Tabelle für Github usw.
cursor.execute("""
CREATE TABLE IF NOT EXISTS profiles (
    user_id INTEGER PRIMARY KEY,
    github TEXT
)
""")

db.commit()

moderation.setup(tree, db)
quiz.setup(tree, db)
stats.setup(tree, db)
encrypt.algorithm(tree, db)
resolve.setup(tree)
ip.ip_infos(tree)
domain.whoisdomain(tree)
domain_lookup.lookup(tree)
roles.setup(tree)
reaction_roles.setup(tree)
portscan.setup(tree)
github.setup(tree, db)


@client.event
async def on_ready():
    await tree.sync()
    print(f"Online als {client.user}")

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")

    if channel is None:
        channel = member.guild.system_channel

    if channel:
        await channel.send(f"👋 Willkommen bei infra.hex, {member.mention}!")


@client.event
async def on_message(message):

    await message_handler.handle_message(
        message,
        quiz,
        cursor,
        db
    )

if __name__ == "__main__":
    print("Bot startet...")
    client.run(TOKEN)