# ChatGPT Console UI

This is a simple command-line tool for managing chat conversations using SQLite and the OpenAI ChatGPT chat model. The
tool allows you to create, list, remove, and interact with different conversations stored in a single SQLite database.

### Installation

#### Prerequisites

- Python 3.7 or higher
- Pip (Python package manager)

#### Setup

Before using the script, you need to install it as a package using pip:

Navigate to the project directory and run:

```bash
pip install -e .
```

This command installs the package in editable mode, which allows you to make changes to the package and have them
reflected without reinstalling the package.

### Usage

After installing the package, you can use it as follows:

```bash
assistant [arguments]
```
Replace `[arguments]` with the appropriate command-line arguments for your script, such as `-l`, `-r`, or `-s`.

Available arguments

- `-l`, `--list`: List all conversations in the database
- `-r`, `--remove`: Remove the specified conversation by its name
- `-s`, `--start`: Start a specified conversation or create a new one with the given name

#### Examples

List all conversations:

```bash
assistant --list
```

Remove a conversation named "example":

```bash
assistant --remove example
```

Start a conversation named "example":

```bash
assistant --start example
```
