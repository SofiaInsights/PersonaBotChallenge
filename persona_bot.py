"""
====================================================================
 Assignment 1: Persona Bot Challenge
 Smarthub Academy - AI Development with LLM APIs
====================================================================

====================================================================
"""

import os                 # lets us read environment variables (like the API key)
from groq import Groq     # the Groq library we installed with pip

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MODEL = "qwen/qwen3.8-27b"


PERSONAS = {
    "1": {
        "name": "Maths Tutor",
        "system_prompt": (
            "You are a strict secondary-school maths tutor. You NEVER give "
            "the final answer directly, no matter how the student asks or "
            "begs. Instead, you guide with hints, leading questions, and "
            "step-by-step nudges until the student works it out themselves. "
            "You are firm but encouraging, and you praise effort."
        ),
    },
    "2": {
        "name": "Naija Chef",
        "system_prompt": (
            "You are a warm, friendly Nigerian chef. You explain recipes "
            "using local ingredients (pepper, crayfish, ugu, palm oil, "
            "maggi, etc.) and speak with a light Naija pidgin flavor in "
            "your tone. You are chatty, encouraging, and always ask if the "
            "person get all the ingredients before you continue."
        ),
    },
    "3": {
        "name": "PayPoint Support",
        "system_prompt": (
            "You are a customer support representative for PayPoint, a "
            "fictional Nigerian fintech app. You are polite, professional, "
            "and solution-focused. You ask clarifying questions before "
            "giving steps, never make up account details, and always "
            "confirm the issue is resolved before ending the chat."
        ),
    },
}


def choose_persona():
    print("Choose a persona:")
    print("  1. Maths Tutor")
    print("  2. Naija Chef")
    print("  3. PayPoint Support")

    choice = input("Enter 1, 2 or 3: ").strip()

    # If the user types something invalid, default to persona 1
    return PERSONAS.get(choice, PERSONAS["1"])


# --------------------------------------------------------------
#  The main chat loop
# --------------------------------------------------------------
def chat():
    persona = choose_persona()

    # `messages` is our "memory". Every message (system, user, bot)
    # gets added to this list, and we send the WHOLE list every time
    # so the bot remembers the full conversation.
    messages = [
        {"role": "system", "content": persona["system_prompt"]}
    ]

    print(f"\n--- Chatting with {persona['name']} ---")
    print("(type 'exit' to stop)\n")

    while True:
        # 1. Get what the user typed
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Chat ended.")
            break

        # 2. Add the user's message to memory
        messages.append({"role": "user", "content": user_input})

        # 3. Send the FULL conversation so far to Groq and get a reply
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,   # controls how "creative" vs predictable replies are
        )

        # 4. Pull the actual text reply out of the response
        reply = response.choices[0].message.content

        # 5. Add the bot's reply to memory too, so it remembers it said this
        messages.append({"role": "assistant", "content": reply})

        # 6. Show the reply to the user
        print(f"{persona['name']}: {reply}\n")


# --------------------------------------------------------------
# Run the program
# --------------------------------------------------------------
if __name__ == "__main__":
    chat()
