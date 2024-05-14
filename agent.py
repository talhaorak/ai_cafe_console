from openai import OpenAI


class Agent:
    def __init__(self, room, name, description, color) -> None:
        self.client = OpenAI()
        self.room = room
        self.name = name
        self.color = color
        self.system_message = {"role": "system",
                               "content": f'Your name is {name}. {description}'
                               }

    async def send_message(self, messages):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        ai_msg = response.choices[0].message.content
        return ai_msg
