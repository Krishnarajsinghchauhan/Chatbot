import json
import os

# File to store AI memory (facts and user details)
MEMORY_FILE = "brain_memory.json"

def load_memory():
    """Load memory (facts) from the JSON file; if not found, return an empty dict."""
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_memory(memory):
    """Save the memory (facts) dictionary to the JSON file."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def add_fact(key, value):
    """
    Add or update a fact in memory.
    For example, key could be 'friend', and value 'Ishant'.
    """
    memory = load_memory()
    memory[key.lower()] = value
    save_memory(memory)
    return f"I've noted that {key} is {value}."

def get_fact(key):
    """
    Retrieve a fact from memory by key.
    For example, if key is 'ishant', and if stored under 'friend': 'Ishant'
    then it returns a custom response.
    """
    memory = load_memory()
    # Simple example: if key is mentioned in memory, return a custom phrase.
    key_lower = key.lower()
    if key_lower in memory:
        # Customize the response as needed
        return f"{memory[key_lower]} is one of your best friends."
    else:
        return None

def process_memory_command(command):
    """
    Process a command that teaches the AI a fact.
    For example, if the user says:
    'my friend name is Ishant' or 'my friend Ishant'
    we try to parse and store that info.
    """
    # Very simple parsing (you can extend this logic as needed)
    command = command.lower()
    if "my friend name is" in command:
        fact = command.split("my friend name is")[-1].strip()
        if fact:
            # Store under key 'friend'
            return add_fact("friend", fact)
    elif "my friend" in command:
        fact = command.split("my friend")[-1].strip()
        if fact:
            return add_fact("friend", fact)
    return None

def answer_memory_query(command):
    """
    Answer queries that ask about previously stored facts.
    For example, if the user asks, 'how is Ishant'
    and we know the friend is Ishant, return a custom response.
    """
    command = command.lower()
    # Look for a query about a friend
    if "how is" in command:
        # Extract the name after "how is"
        name = command.split("how is")[-1].strip()
        fact = get_fact(name)
        if fact:
            return fact
    return None
