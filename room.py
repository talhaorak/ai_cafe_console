import asyncio
import aioconsole
from collections import namedtuple
from colored import Fore


ChatMessage = namedtuple("ChatMessage", ["sender", "message"])

PASS = "pass"


class Room:
    def __init__(self, username="User"):
        self.username = username
        self.agents = {}
        self.history = []
        self.send_queue = asyncio.Queue()

    def add_agent(self, agent):
        self.agents[agent.name] = agent

    def remove_agent(self, agent):
        del self.agents[agent.name]

    def room_status(self, for_agent=None):
        statusStr = f"""You are in a chat room. There are {len(self.agents)} other participants in the room. 
        Their names are: {self.username}, """
        for i, agent_name in enumerate(self.agents):
            if for_agent and agent_name == for_agent:
                continue
            agent = self.agents[agent_name]
            statusStr += f"{agent.name}"
            if i == len(self.agents) - 2:
                statusStr += " and "
            elif i == len(self.agents) - 1:
                statusStr += "."
            else:
                statusStr += ", "
        statusStr += f""" If you don't think you've got anything to say, just reply with {PASS} and nothing else. 
        In your responses, don't include your name at the beginning of the sentence.
        """
        # If you want to refer to someone, use their name with an at sign (@). Example: "@Jacob, how are you?"
        # If you see your name with an at sign, it means someone is talking to you.
        return statusStr

    async def add_task(self, message, sender=""):
        if not sender:
            sender = self.username
        # await aioconsole.aprint(f"{Fore.dark_gray} {sender} wants to send {message}")
        task = ChatMessage(sender, message)
        await self.send_queue.put(task)

    async def run(self):
        while True:
            task = await self.send_queue.get()
            await self.broadcast(task)

    async def broadcast(self, msg):

        self.history.append(msg)

        for agent in self.agents.values():
            if agent.name == msg.sender:
                continue
            initial_msg = agent.system_message
            initial_msg["content"] += f" {self.room_status(agent.name)}"
            messages = [initial_msg] + \
                self.format_messages_for_agent(agent.name)
            # await aioconsole.aprint(f"{Fore.dark_gray} Sending message to {agent.name}: ({msg.sender} {msg.message})")
            response = await agent.send_message(messages)
            nResponse = response.replace(".", "").lower()
            await aioconsole.aprint(f"{agent.color}{agent.name}: {response}")
            if nResponse != PASS:
                await self.add_task(response, agent.name)

    def format_messages_for_agent(self, agent_name):
        messages = []
        for entry in self.history:
            if entry.sender == self.username:
                messages.append(
                    {"role": "user", "content": f"{self.username}: {entry.message}"})
            elif entry.sender == agent_name:
                messages.append(
                    {"role": "assistant", "content": entry.message})
            else:
                messages.append(
                    {"role": "user", "content": f"{entry.sender}: {entry.message}"})
        return messages
