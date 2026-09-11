"""
AECHO - Intro Module
Handles the very first boot experience: introduces itself, sets up the
first owner (name + password), and greets a returning owner on later boots.
"""

import brain
import voice


def run_intro(memory):
    """
    Called once at app start (from main.py).
    Decides whether this is a first-ever boot or a returning owner,
    and returns the text to display in the chat log.
    """
    if brain.is_first_run(memory):
        return _first_boot_sequence(memory)
    else:
        return _returning_owner_greeting(memory)


def _first_boot_sequence(memory):
    """
    Runs only once, when AECHO has no owner yet.
    Introduces itself, then asks for the new owner's name and a password.
    """
    intro_lines = [
        "Hello world, I just born.",
        f"I am AECHO, {brain.CREATOR_NAME}'s Enhanced Cognitive Handling Operator.",
        f"My creator is {brain.CREATOR_NAME}."
    ]

    for line in intro_lines:
        voice.speak(line)

    # Combine into one block for the chat log display
    return "\n".join(intro_lines)


def complete_first_setup(memory, owner_name, owner_password):
    """
    Called after the user replies with their name and sets a password
    following the first-boot intro. Finalizes ownership setup.
    """
    brain.set_owner(memory, owner_name, owner_password)
    confirmation = f"Nice to meet you, {owner_name}. You are now my owner."
    voice.speak(confirmation)
    return confirmation


def _returning_owner_greeting(memory):
    """Simple greeting for normal boots after setup is already done."""
    owner = memory.get("owner", "there")
    greeting = f"Welcome back, {owner}."
    voice.speak(greeting)
    return greeting
