import os
import openai
from dotenv import load_dotenv, find_dotenv




def chat_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    openai.api_key = os.environ["API_KEY"]

    while True:
        user_input = input("User: ")
        prompt = f"{user_input}\nChatGPT:"
        response = chat_gpt(prompt)
        print("ChatGPT:", response)
