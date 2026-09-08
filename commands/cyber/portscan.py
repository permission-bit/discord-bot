import discord
from discord import app_commands
import nmap
import asyncio


def setup(tree):

    @tree.command(
        name="portscan",
        description="Scannt ein erlaubtes Testziel"
    )
    async def portscan(interaction: discord.Interaction):

        await interaction.response.defer()

        target = "scanme.nmap.org"


        def run_scan():

            scanner = nmap.PortScanner()

            scanner.scan(
                target,
                arguments="-p 22,21,80,8080,445 -sT --open",
                timeout=60
            )

            result = ""

            for host in scanner.all_hosts():

                result += f"Host: {host}\n"

                if "tcp" in scanner[host]:

                    for port, info in scanner[host]["tcp"].items():

                        result += (
                            f"Port: {port}\n"
                            f"Status: {info['state']}\n"
                            f"Service: {info['name']}\n\n"
                        )

            return result


        try:

            result = await asyncio.to_thread(
                run_scan
            )


            if not result:
                result = "Keine offenen Ports gefunden."


            embed = discord.Embed(
                title="🔍 Portscan Ergebnis",
                description=f"```{result[:4000]}```",
                color=discord.Color.green()
            )


            await interaction.followup.send(
                embed=embed
            )


        except Exception as e:

            await interaction.followup.send(
                f"❌ Fehler: {e}"
            )