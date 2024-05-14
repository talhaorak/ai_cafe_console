import asyncio

from dotenv import load_dotenv
from openai import OpenAI
from colored import Fore

from agent import Agent
from room import Room
from cli import cli

load_dotenv()

username = input("Enter your name: ")


async def main():
    room = Room(username)
    alice = Agent(room, "Alice",
                  "You're a helpful and playful assistant.", Fore.magenta)
    bob = Agent(
        room, "Bob", "You're a helpful and serious assistant.", Fore.cyan)

    room.add_agent(alice)
    room.add_agent(bob)

    room_coroutine = asyncio.create_task(room.run())
    cli_coroutine = asyncio.create_task(cli(username, room))
    await asyncio.gather(room_coroutine, cli_coroutine)


asyncio.run(main())
