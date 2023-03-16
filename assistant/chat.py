import os

import cursor
import openai
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from rich.console import Console
from rich.text import Text

from .database import insert_message, load_conversation_history, create_conversation


def prompt_continuation(width, line_number, is_soft_wrap):
    return '> '


def start_chat(conn, conversation_name, init_prompt):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    conversation_id = create_conversation(conn, conversation_name)
    messages = load_conversation_history(conn, conversation_id)

    cursor.show()
    console = Console()
    console.print(Text.from_markup("\n" * console.height), end="", soft_wrap=True)
    print("ESC+Enter to send")

    prompt_session = PromptSession()
    while True:
        text_from_user = prompt_session.prompt('\n> ',
                                               multiline=True,
                                               prompt_continuation=prompt_continuation,
                                               auto_suggest=AutoSuggestFromHistory()
                                               )
        print()

        messages.append({
            "role": "user",
            "content": text_from_user
        })
        insert_message(conn, conversation_id, "user", text_from_user)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            stream=True
        )

        role = None
        delta_contents = []

        for chunk in response:
            role = role or chunk.choices[0].delta.get("role")
            delta_content = chunk.choices[0].delta.get("content")
            if delta_content:
                console.print(delta_content, end="", soft_wrap=True)
                delta_contents.append(delta_content)
                console.file.flush()
        print()

        reply = "".join(delta_contents)
        messages.append({
            "role": role,
            "content": reply
        })
        insert_message(conn, conversation_id, role, reply)
