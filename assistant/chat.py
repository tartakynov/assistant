import os
from sys import stdout

import openai

from .database import insert_message, load_conversation_history, create_conversation


def start_chat(conn, conversation_name):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    conversation_id = create_conversation(conn, conversation_name)
    messages = load_conversation_history(conn, conversation_id)

    if messages:
        print(f"Loaded an existing conversation with {len(messages)} messages")
    else:
        print("Started an empty conversation")
    print()

    while True:
        text_from_user = input("User: ")
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

        stdout.write("ChatGPT: ")
        for chunk in response:
            role = role or chunk.choices[0].delta.get("role")
            delta_content = chunk.choices[0].delta.get("content")
            if delta_content:
                stdout.write(delta_content)
                delta_contents.append(delta_content)
        stdout.write("\n")

        reply = "".join(delta_contents)
        messages.append({
            "role": role,
            "content": reply
        })
        insert_message(conn, conversation_id, role, reply)