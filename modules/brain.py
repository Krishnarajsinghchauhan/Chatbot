import json
import os
import re

MEMORY_FILE = "modules/memory.json"

def ensure_memory_file():
    """Ensure the memory file exists; if not, create it with an empty dictionary."""
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w") as f:
            json.dump({}, f)

# Create the memory file upon module load
ensure_memory_file()

def load_memory():
    """Load the brain memory from the JSON file. Returns a dictionary."""
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_memory(memory):
    """Save the brain memory (a dictionary) to the JSON file."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def add_fact(category, fact):
    """
    Add or update a fact in the brain memory under a given category.
    This ensures that the value stored is always a list of facts.
    Returns a confirmation message.
    """
    memory = load_memory()
    cat = category.lower()
    # If category exists but is not a list, convert it to list
    if cat in memory and not isinstance(memory[cat], list):
        memory[cat] = [memory[cat]]
    if cat in memory:
        # Only add if the fact is not already present (case-insensitive check)
        if fact.lower() not in [x.lower() for x in memory[cat]]:
            memory[cat].append(fact)
    else:
        memory[cat] = [fact]
    save_memory(memory)
    return f"Okay, I've noted that {cat} includes {fact}."

def get_fact(category):
    """
    Retrieve facts from the brain memory by category.
    Returns the facts as a comma-separated string if found.
    """
    memory = load_memory()
    cat = category.lower()
    if cat in memory and isinstance(memory[cat], list) and memory[cat]:
        facts = memory[cat]
        if len(facts) == 1:
            return facts[0]
        else:
            return ", ".join(facts[:-1]) + ", and " + facts[-1]
    return None

def process_memory_input(command):
    """
    Process commands intended to teach the AI new facts.
    Recognized patterns include details for:
      - friend / best friend / friends with benefits
      - favorite food
      - favorite place
      - family
      - relationship status, girlfriend, boyfriend, etc.
    Returns a confirmation message if a fact is stored; otherwise, returns None.
    """
    command = command.strip().lower()

    # Patterns for friend-related facts
    friend_patterns = [
        r"my friend name is\s+(.*)",
        r"remember that my friend(?: is)?\s+(.*)",
        r"(.*)\s+is my friend",
        r"my best friend(?:'s)? name is\s+(.*)"
    ]
    for pattern in friend_patterns:
        match = re.search(pattern, command)
        if match:
            name = match.group(1).strip()
            if name:
                return add_fact("friend", name)

    # Patterns for favorite food
    food_patterns = [
        r"my (?:favourite|favorite) food(?: is)?\s+(.*)",
        r"i love (?:eating|food)\s+(.*)"
    ]
    for pattern in food_patterns:
        match = re.search(pattern, command)
        if match:
            food = match.group(1).strip()
            if food:
                return add_fact("favorite food", food)

    # Patterns for favorite place
    place_patterns = [
        r"my (?:favourite|favorite) place(?: is)?\s+(.*)",
        r"i love (?:visiting|being in)\s+(.*)"
    ]
    for pattern in place_patterns:
        match = re.search(pattern, command)
        if match:
            place = match.group(1).strip()
            if place:
                return add_fact("favorite place", place)

    # Patterns for family details
    family_patterns = [
        r"my family(?: is)?\s+(.*)",
        r"remember that my family(?: is)?\s+(.*)"
    ]
    for pattern in family_patterns:
        match = re.search(pattern, command)
        if match:
            fam = match.group(1).strip()
            if fam:
                return add_fact("family", fam)

    # Patterns for relationship status, girlfriend, boyfriend
    relationship_patterns = [
        r"my (girlfriend|boyfriend) name is\s+(.*)",
        r"i am (single|married|in a relationship)",
        r"remember that my (girlfriend|boyfriend) is\s+(.*)"
    ]
    for pattern in relationship_patterns:
        match = re.search(pattern, command)
        if match:
            # For relationship status with one group or two groups
            if len(match.groups()) == 1:
                status = match.group(1).strip()
                return add_fact("relationship", status)
            elif len(match.groups()) >= 2:
                relation = match.group(1).strip()
                name = match.group(2).strip()
                return add_fact(relation, name)

    return None

def answer_memory_query(command):
    """
    Process queries that ask about stored facts.
    Examples:
      - "who is my friend?"
      - "what is my favorite food?"
      - "tell me about my family"
      - "what is my relationship status?"
    Returns a human-like response if a fact is found, otherwise returns None.
    """
    command = command.strip().lower()

    # Query for friend-related info
    if any(q in command for q in ["who is my friend", "how is my friend", "friend"]):
        fact = get_fact("friend")
        if fact:
            return f"Your friend is {fact}."
    # Query for favorite food
    if any(q in command for q in ["favorite food", "favourite food", "what do i like to eat"]):
        fact = get_fact("favorite food")
        if fact:
            return f"Your favorite food is {fact}."
    # Query for favorite place
    if any(q in command for q in ["favorite place", "favourite place", "where do i like to go"]):
        fact = get_fact("favorite place")
        if fact:
            return f"Your favorite place is {fact}."
    # Query for family
    if any(q in command for q in ["family", "my family"]):
        fact = get_fact("family")
        if fact:
            return f"You cherish your family: {fact}."
    # Query for relationship
    if any(q in command for q in ["relationship", "girlfriend", "boyfriend"]):
        # Check for relationship and specific ones
        rel_status = get_fact("relationship")
        gf = get_fact("girlfriend")
        bf = get_fact("boyfriend")
        response_parts = []
        if rel_status:
            response_parts.append(f"your relationship status is {rel_status}")
        if gf:
            response_parts.append(f"your girlfriend is {gf}")
        if bf:
            response_parts.append(f"your boyfriend is {bf}")
        if response_parts:
            return " and ".join(response_parts) + "."
    return None

def process_brain_command(command):
    """
    Determine if the command is intended for the AI's brain.
    If it's a teaching command, store the fact and return a confirmation.
    If it's a query, retrieve the stored fact and return a response.
    Returns a response string if handled, or None if not a brain command.
    """
    # First, try to store new information
    response = process_memory_input(command)
    if response:
        return response
    # Next, try to answer a query based on stored memory
    response = answer_memory_query(command)
    return response

# For testing purposes:
if __name__ == "__main__":
    # Teach the AI some facts
    print(process_brain_command("My friend name is Ishant"))
    print(process_brain_command("My favorite food is pizza"))
    print(process_brain_command("My favorite place is Paris"))
    print(process_brain_command("My girlfriend name is Anjali"))
    print(process_brain_command("I am married"))
    # Query the memory
    print(process_brain_command("Who is my friend?"))
    print(process_brain_command("What is my favorite food?"))
    print(process_brain_command("Tell me about my family"))
    print(process_brain_command("What is my relationship?"))
