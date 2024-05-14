import os
import sys
import asyncio
import aioconsole
from colored import Fore, stylize_interactive


async def cli(username, room):
    sys.ps1 = stylize_interactive(f"{username}: ", Fore.blue)
    while True:
        user_input = await aioconsole.ainput(sys.ps1)
        try:
            await room.add_task(user_input)
        except Exception as e:
            print(e)
