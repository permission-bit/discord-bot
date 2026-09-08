# infra.hex Discord Bot

A modular **Discord bot written in Python** with a focus on server management, community features, developer utilities, cybersecurity-related lookups, quizzes, profiles, and moderation.

The bot uses **discord.py**, **SQLite**, and several external Python libraries and APIs. Its command system is organized into separate modules, making it easy to extend and maintain.

---

## ✨ Features

### 🛡️ Moderation

The bot provides several moderation commands:

- Ban members
- Kick members
- Warn members
- Delete messages
- Add and remove roles
- Protected users that cannot be banned or kicked
- Discord permission checks
- Role hierarchy protection

### 🔐 Cyber / Network Utilities

The bot includes several security and networking utilities designed for legitimate administration, testing, and educational purposes:

- DNS A-record lookup
- WHOIS domain lookup
- IP information lookup
- Hostname resolution
- Hash generation
- Port scanning of the configured test target

> **Important:** Network and security features should only be used against systems and domains that you own or have explicit permission to test.

### 🧠 Quiz System

A built-in quiz system with three difficulty levels:

- Easy
- Medium
- Hard

Players receive points for correct answers, which are stored in SQLite.

The bot also provides a leaderboard showing the top 10 players.

### 🎭 Reaction / Role Selection

Users can select interest roles through an interactive Discord dropdown menu.

Currently supported roles:

- 🐍 Python
- 🔐 Security
- 💻 Developer

Users can also remove their selected role by selecting it again.

### 👤 User Profiles

Users can link their GitHub profile to their Discord account.

The bot stores the GitHub URL in the SQLite database and displays it through the `/profil` command.

### 📊 Server Statistics

The `/stats` command displays information about the current Discord server, including:

- Member count
- Online members
- Humans
- Bots
- Text channels
- Voice channels
- Categories
- Boost level
- Number of boosts
- Server creation date

### 👋 Welcome System

When a new member joins a server, the bot attempts to send a welcome message in:

1. `#general`
2. The server's system channel

---

# 📁 Project Structure

```text
.
├── README.md
├── bot.py
├── requirements.txt
├── daemon.txt
│
├── commands
│   ├── README.md
│   ├── __init__.py
│   │
│   ├── cyber
│   │   ├── domain.py
│   │   ├── domain_lookup.py
│   │   ├── encrypt.py
│   │   ├── ip.py
│   │   ├── portscan.py
│   │   └── resolve.py
│   │
│   ├── events
│   │   └── messages.py
│   │
│   ├── fun
│   │   ├── __init__.py
│   │   └── quiz.py
│   │
│   ├── moderation
│   │   ├── __init__.py
│   │   ├── ban.py
│   │   ├── clear.py
│   │   ├── kick.py
│   │   ├── logs.py
│   │   ├── reaction_roles.py
│   │   ├── roles.py
│   │   └── warn.py
│   │
│   ├── profile
│   │   └── github.py
│   │
│   └── server
│       └── stats.py
```

---

# 🧩 Architecture

The project uses a modular command architecture.

Instead of putting every command into `bot.py`, commands are separated into functional modules.

For example:

```text
commands/
├── cyber/
├── moderation/
├── fun/
├── profile/
└── server/
```

Each command module exposes a `setup()` function that receives the Discord `CommandTree`.

Example:

```python
def setup(tree):

    @tree.command(
        name="example",
        description="Example command"
    )
    async def example(interaction: discord.Interaction):

        await interaction.response.send_message(
            "Hello!"
        )
```

The main `bot.py` file then loads the module:

```python
example.setup(tree)
```

This approach makes the bot easier to expand without turning `bot.py` into a large monolithic file.

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_DIRECTORY>
```

---

## 2. Create a virtual environment

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

---

## 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

The project currently depends on libraries such as:

- `discord.py`
- `dnspython`
- `python-whois`
- `requests`
- `python-nmap`
- `python-dotenv`

---

# 🔧 Additional System Requirements

The port scanning module uses **Nmap** through the Python `nmap` package.

Installing the Python package alone is not enough. The Nmap executable must also be installed on the machine running the bot.

### Debian / Ubuntu

```bash
sudo apt update
sudo apt install nmap
```

### Arch Linux

```bash
sudo pacman -S nmap
```

### macOS

```bash
brew install nmap
```

### Windows

Install Nmap from the official Nmap website.

---

# 🔑 Discord Bot Configuration

Create a Discord application and bot through the Discord Developer Portal.

The bot token should **never be hard-coded into the source code**.

This project loads the token from an environment variable:

```python
load_dotenv()

TOKEN = os.getenv("TOKEN")
```

Create a `.env` file in the project root:

```env
TOKEN=YOUR_DISCORD_BOT_TOKEN
```

Replace:

```text
YOUR_DISCORD_BOT_TOKEN
```

with your actual bot token.

### ⚠️ Never commit `.env`

Add the following to `.gitignore`:

```gitignore
.env
.venv/
venv/
__pycache__/
*.pyc
bot.db
```

If your bot token is accidentally exposed, immediately regenerate it through the Discord Developer Portal.

---

# 🤖 Discord Intents

The bot currently enables:

```python
intents = discord.Intents.default()

intents.message_content = True
intents.members = True
```

Therefore, the corresponding privileged intents should be enabled in the Discord Developer Portal.

The bot uses:

### Message Content Intent

Required for message-based commands such as:

```text
!ping
!hilfe
!info
!server
!würfel
!zeit
```

It is also used by the quiz system to process answers.

### Server Members Intent

Required for functionality involving server members, including:

- Member information
- Welcome messages
- Role management
- Member statistics

---

# 📜 Commands

## 💬 General Commands

| Command   | Description                              |
| --------- | ---------------------------------------- |
| `!ping`   | Tests whether the bot is responding      |
| `!hilfe`  | Displays the command overview            |
| `!info`   | Displays information about yourself      |
| `!server` | Displays basic server information        |
| `!würfel` | Rolls a random number from 1–6           |
| `!zeit`   | Displays the current server process time |

The bot also responds to messages containing:

```text
hallo
python
discord
```

---

# 🛡️ Moderation Commands

## `/ban`

Bans a Discord member.

```text
/ban user:<member> reason:<reason>
```

Requires:

```text
Ban Members
```

The bot also supports protected users through:

```python
PROTECTED_USERS
```

Protected users cannot be banned.

---

## `/kick`

Kicks a Discord member.

```text
/kick user:<member> reason:<reason>
```

Requires:

```text
Kick Members
```

Protected users cannot be kicked.

---

## `/warn`

Creates a warning for a member.

```text
/warn user:<member> reason:<reason>
```

Warnings are stored in the SQLite database.

The warning table contains:

```text
id
user_id
moderator_id
reason
timestamp
```

---

## `/clear`

Deletes messages from the current channel.

```text
/clear amount:<number>
```

The amount must be between:

```text
1–100
```

Requires:

```text
Manage Messages
```

---

## `/addrole`

Adds a role to a member.

```text
/addrole user:<member> rolle:<role>
```

Requires:

```text
Manage Roles
```

The bot also checks its own role hierarchy.

The target role must be below the bot's highest role.

---

## `/removerole`

Removes a role from a member.

```text
/removerole user:<member> rolle:<role>
```

Requires:

```text
Manage Roles
```

---

# 🎭 Role Menu

## `/rollenmenü`

Creates an interactive role-selection menu.

Available roles:

```text
🐍 Python
🔐 Security
💻 Developer
```

Selecting a role adds it to the user.

Selecting the same role again removes it.

The roles must already exist on the Discord server.

The bot must also have permission to manage those roles.

---

# 🔐 Cyber / Network Commands

These commands are intended for legitimate administration, troubleshooting, research, and authorized security testing.

---

## `/dns`

Performs a DNS A-record lookup.

```text
/dns domain:example.com
```

Example:

```text
/dns domain:openai.com
```

The bot resolves the domain and displays the IPv4 addresses returned by the DNS server.

---

## `/whois`

Performs a WHOIS lookup for a domain.

```text
/whois domain:example.com
```

The command attempts to display:

- Domain
- Registrar
- Creation date
- Expiration date

WHOIS data can vary depending on the registry and domain.

---

## `/ip`

Retrieves information about an IPv4 address through the IPinfo API.

```text
/ip ip:8.8.8.8
```

The bot attempts to display:

- IP address
- City
- Region
- Country
- Organization

The accuracy of geolocation and organization information depends on the external IP information provider.

---

## `/resolve`

Resolves a hostname to an IPv4 address.

```text
/resolve host:example.com
```

The command uses Python's socket resolver.

Example:

```text
example.com → 93.184.216.34
```

---

## `/hash`

Calculates several cryptographic hashes from text.

```text
/hash text:Hello World
```

Currently generated:

```text
MD5
SHA1
SHA256
```

Example output:

```text
MD5
<hash>

SHA1
<hash>

SHA256
<hash>
```

> MD5 and SHA-1 are considered unsuitable for modern collision-resistant security applications. They are included here primarily for educational, compatibility, and identification purposes. SHA-256 should generally be preferred for new security-sensitive applications.

---

## `/portscan`

Runs a TCP port scan against the configured test target.

The current implementation uses:

```text
scanme.nmap.org
```

and scans:

```text
21
22
80
445
8080
```

The scanner uses:

```text
-sT
--open
```

Results include:

- Host
- Port
- State
- Service

### Authorization

Only scan systems that you own or have explicit permission to test.

The current target is intended as an authorized Nmap testing target. If you change the target, make sure you have permission to scan it.

---

# 🧠 Quiz System

The bot includes an interactive quiz system.

## `/quiz`

Starts a quiz.

```text
/quiz schwierigkeitsgrad:einfach
```

Available difficulty levels:

```text
einfach
mittel
schwer
```

Players answer by sending:

```text
1
2
3
4
```

### Points

| Difficulty | Points |
| ---------- | -----: |
| Easy       |      5 |
| Medium     |     10 |
| Hard       |     20 |

Correct answers are added to the player's score.

---

## `/rangliste`

Displays the top 10 players.

```text
/rangliste
```

Scores are stored in the SQLite database.

---

# 👤 Profile System

## `/github`

Links a GitHub profile to the current Discord user.

```text
/github link:https://github.com/username
```

The profile is stored in SQLite.

---

## `/profil`

Displays the current user's profile.

```text
/profil
```

Currently the profile can contain:

```text
🐙 GitHub
```

---

# 📊 Server Statistics

## `/stats`

Displays server statistics.

```text
/stats
```

The command reports:

```text
Members
Online
Bots
Humans
Text Channels
Voice Channels
Categories
Boost Level
Server Boosts
```

---

# 👤 User Information

## `/userinfo`

Displays information about a Discord member.

```text
/userinfo
```

or:

```text
/userinfo user:<member>
```

The embed includes:

- Username
- User ID
- Server join date
- Display avatar

---

# 💾 Database

The bot uses **SQLite** for persistent data storage.

The database file is:

```text
bot.db
```

Currently used tables include:

## `scores`

Stores quiz scores.

```text
user_id
username
points
```

---

## `profiles`

Stores user profiles.

```text
user_id
github
```

---

## `warnings`

Stores moderation warnings.

```text
id
user_id
moderator_id
reason
timestamp
```

The database is automatically initialized when the corresponding modules are loaded.

---

# 📦 Requirements

A typical `requirements.txt` for the current project should contain:

```text
discord.py
dnspython
python-whois
requests
python-nmap
python-dotenv
```

Install everything with:

```bash
pip install -r requirements.txt
```

For reproducible deployments, it is recommended to pin tested versions in `requirements.txt`.

---

# ▶️ Running the Bot

After installing the dependencies and configuring `.env`, start the bot with:

```bash
python bot.py
```

You should see:

```text
Bot startet...
```

followed by something similar to:

```text
Online als <bot-name>
```

Once the bot is online, the application command tree is synchronized with Discord.

---

# 🐧 Running as a Linux Service

For a permanent Linux deployment, the bot can be run using a process manager such as `systemd`.

A typical service can look like:

```ini
[Unit]
Description=infra.hex Discord Bot
After=network.target

[Service]
WorkingDirectory=/path/to/infra.hex
ExecStart=/path/to/infra.hex/.venv/bin/python bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Save the service as:

```text
/etc/systemd/system/infra-hex.service
```

Then run:

```bash
sudo systemctl daemon-reload
sudo systemctl enable infra-hex
sudo systemctl start infra-hex
```

Check the status:

```bash
sudo systemctl status infra-hex
```

View logs:

```bash
journalctl -u infra-hex -f
```

Adjust the paths to match your installation.

---

# 🔐 Security Considerations

Because this bot contains network and security-related functionality, deployment should follow basic security practices.

### Never expose the bot token

Do not put the token directly into:

```python
client.run("TOKEN_HERE")
```

Use environment variables instead.

---

### Protect `.env`

Make sure `.env` is excluded from Git:

```gitignore
.env
```

---

### Protect the SQLite database

The database can contain:

- User IDs
- Usernames
- Quiz scores
- GitHub profiles
- Moderation warning information

Treat the database as application data and avoid publicly exposing it.

---

### Restrict bot permissions

Only grant the bot the permissions it actually needs.

For example, moderation functionality may require:

```text
Ban Members
Kick Members
Manage Messages
Manage Roles
```

Avoid granting unnecessary administrator privileges.

---

### Role hierarchy

Discord prevents bots from managing roles that are higher than or equal to the bot's highest role.

Therefore, the bot's role should be positioned above the roles it needs to manage.

Example:

```text
Administrator
Bot
Developer
Security
Python
@everyone
```

---

# ⚠️ Cybersecurity Disclaimer

The network-related functionality in this project is intended for:

- Educational purposes
- System administration
- Troubleshooting
- Security research
- Authorized testing

Do **not** use the bot to scan, attack, enumerate, or otherwise interact with systems without authorization.

You are responsible for complying with all applicable laws, regulations, network policies, and terms of service.

The project author is not responsible for misuse of the software.

---

# 🧱 Extending the Bot

The modular structure makes it relatively simple to add new commands.

For example, create:

```text
commands/fun/example.py
```

Then implement:

```python
import discord
from discord import app_commands


def setup(tree):

    @tree.command(
        name="example",
        description="Example command"
    )
    async def example(
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(
            "Hello from infra.hex!"
        )
```

Import it in `bot.py`:

```python
from commands.fun import example
```

Then register it:

```python
example.setup(tree)
```

After restarting the bot, the command will be synchronized with Discord.

---

# 🧪 Development

Recommended development environment:

```text
Python 3.10+
discord.py
SQLite
Nmap
```

Before deploying changes:

1. Test commands on a development Discord server.
2. Verify bot permissions.
3. Test error handling.
4. Check database changes.
5. Verify that `.env` and database files are not committed.
6. Test security-related functionality only against authorized targets.

---

# 🐛 Troubleshooting

## Slash commands are not appearing

Try restarting the bot and make sure:

```python
await tree.sync()
```

is executed successfully.

Also verify that the bot was invited with the appropriate application command scope.

---

## `ModuleNotFoundError`

Install the project's dependencies:

```bash
pip install -r requirements.txt
```

If you are using a virtual environment, make sure it is activated.

---

## Nmap errors

Make sure the Nmap executable is installed:

```bash
nmap --version
```

If the command cannot be found, install Nmap on the host system.

---

## Bot cannot manage a role

Check:

1. The bot has `Manage Roles`.
2. The target role is below the bot's highest role.
3. The role is not the server's managed/integration role.
4. The bot is operating in the correct server.

---

## Bot cannot read messages

Verify that:

```python
intents.message_content = True
```

is enabled and that the corresponding privileged intent is enabled in the Discord Developer Portal.

---

# 📌 Current Command Overview

| Command       | Category   | Description                 |
| ------------- | ---------- | --------------------------- |
| `!ping`       | General    | Test bot response           |
| `!hilfe`      | General    | Show help                   |
| `!info`       | General    | User information            |
| `!server`     | Server     | Server information          |
| `!würfel`     | Fun        | Roll a dice                 |
| `!zeit`       | Fun        | Show time                   |
| `/userinfo`   | User       | Detailed user information   |
| `/stats`      | Server     | Server statistics           |
| `/quiz`       | Fun        | Start a quiz                |
| `/rangliste`  | Fun        | Quiz leaderboard            |
| `/ban`        | Moderation | Ban a member                |
| `/kick`       | Moderation | Kick a member               |
| `/warn`       | Moderation | Warn a member               |
| `/clear`      | Moderation | Delete messages             |
| `/addrole`    | Moderation | Add a role                  |
| `/removerole` | Moderation | Remove a role               |
| `/rollenmenü` | Roles      | Create role selector        |
| `/hash`       | Cyber      | Generate hashes             |
| `/dns`        | Cyber      | DNS A-record lookup         |
| `/whois`      | Cyber      | WHOIS lookup                |
| `/ip`         | Cyber      | IP information              |
| `/resolve`    | Cyber      | Resolve hostname            |
| `/portscan`   | Cyber      | Scan configured test target |
| `/github`     | Profile    | Save GitHub profile         |
| `/profil`     | Profile    | Display profile             |

---

# 🗺️ Roadmap

Possible future improvements include:

- [ ] Persistent configuration per Discord server
- [ ] Better centralized error handling
- [ ] Moderation logging
- [ ] Warning management commands
- [ ] Temporary bans and mutes
- [ ] Automatic moderation
- [ ] More quiz questions
- [ ] Per-server quiz leaderboards
- [ ] User profile expansion
- [ ] GitHub API integration
- [ ] Better DNS record support
- [ ] IPv6 support
- [ ] Improved permission checks
- [ ] Configuration management
- [ ] Automated tests
- [ ] Docker deployment
- [ ] Structured logging
- [ ] Pagination for large results
- [ ] Better API error handling

---

# 📄 License

Add your preferred license here.

For example:

```text
MIT License
```

If you choose the MIT License, include the complete license text in a `LICENSE` file in the repository.

---

# 🤝 Contributing

Contributions are welcome.

A typical workflow is:

```bash
git checkout -b feature/my-feature
```

Make your changes, test them locally, and commit them:

```bash
git add .
git commit -m "Add my feature"
```

Then push the branch:

```bash
git push origin feature/my-feature
```

Open a pull request with a description of the changes.

Please avoid committing:

```text
.env
bot.db
.venv/
__pycache__/
```

---

# ⭐ About

**infra.hex** is a modular Python Discord bot combining community management, moderation, server utilities, quizzes, user profiles, and authorized cybersecurity/networking tools.

Built with:

- Python
- discord.py
- SQLite
- Nmap
- DNS / WHOIS utilities
- IP information services

---

**Made with Python 🐍 and Discord.py 🤖**
