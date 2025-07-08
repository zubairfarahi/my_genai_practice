import os
from openai import AsyncOpenAI  
import chainlit as cl  
from dotenv import load_dotenv

load_dotenv()

# ChatOpenAI Templates
system_template = """You are a helpful assistant to a university level student. You speak in friendly and professional tone. Your answers are easy to understand, comprehensive, and concise. You can put answers in bullet point format when the answer is a list of items.
"""

user_template = """{input}
Think through your response step by step. Rate your answers out of 5 at the end as if you are a teacher evaluating answers from students. Suggest follow up questions at the end.
"""

@cl.on_chat_start  
async def start_chat():
    settings = {
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 500,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    cl.user_session.set("settings", settings)

@cl.on_message
async def main(message: cl.Message):
    settings = cl.user_session.get("settings")
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    messages = [
        {"role": "system", "content": system_template},
        {"role": "user", "content": user_template.format(input=message.content)},
    ]

    msg = cl.Message(content="")

    stream = await client.chat.completions.create(
        messages=messages, stream=True, **settings
    )
    async for stream_resp in stream:

        token = getattr(stream_resp.choices[0].delta, "content", "")
        await msg.stream_token(token or "")

    await msg.send()
