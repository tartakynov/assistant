import argparse
import os
import sqlite3

from dotenv import load_dotenv, find_dotenv

from .chat import start_chat
from .database import list_conversations, remove_conversation, create_tables


def main():
    parser = argparse.ArgumentParser(description="Interact with conversation database.")
    parser.add_argument("-l", "--list", action="store_true", help="List conversations")
    parser.add_argument("-r", "--remove", help="Remove specified conversation")
    parser.add_argument("-s", "--start", help="Start specified conversation or create a new one with the given name")

    args = parser.parse_args()

    load_dotenv(find_dotenv())

    with sqlite3.connect("chats.db") as conn:
        create_tables(conn)
        if args.list:
            print("\n".join(list_conversations(conn)))
        elif args.remove:
            if remove_conversation(conn, args.remove):
                print(f"Removed conversation '{args.remove}'")
            else:
                print(f"Conversation '{args.remove}' not found")
        elif args.start:
            try:
                start_chat(conn, args.start)
            except KeyboardInterrupt:
                print("\nExiting gracefully...")
        else:
            print("No action specified. Use -h or --help for available options.")


if __name__ == "__main__":
    main()
