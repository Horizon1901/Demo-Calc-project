import json

from calculator import add, subtract
from ollama_client import ask_llm


SYSTEM_PROMPT = """
You are an AI planning engine.

Your ONLY job is to determine:
1. The mathematical operation.
2. The two numbers.

DO NOT calculate the answer.

Return ONLY valid JSON.

Examples:

User: Add 3 and 4

{
    "operation":"add",
    "a":3,
    "b":4
}

User: Subtract 10 and 2

{
    "operation":"subtract",
    "a":10,
    "b":2
}

User: Multiply 6 by 2

{
    "operation":"multiply",
    "a":6,
    "b":2
}

User: Divide 20 by 5

{
    "operation":"divide",
    "a":20,
    "b":5
}

Never explain.

Never use markdown.

Never use ```json.

Return ONLY the JSON object.
"""


def process_prompt(user_prompt: str):

    # Ask Ollama
    response = ask_llm(
        SYSTEM_PROMPT,
        user_prompt
    )

    print("\n========== RAW LLM RESPONSE ==========")
    print(response)
    print("======================================\n")

    # Try converting response into JSON
    try:
        plan = json.loads(response)
    except Exception as e:
        return f"Invalid JSON returned by LLM:\n\n{response}\n\nError:\n{e}"

    operation = plan.get("operation")
    a = plan.get("a")
    b = plan.get("b")

    if operation == "add":
        return str(add(a, b))

    elif operation == "subtract":
        return str(subtract(a, b))

    elif operation == "multiply":

        result = 0

        for _ in range(b):
            result = add(result, a)

        return str(result)

    elif operation == "divide":

        if b == 0:
            return "Cannot divide by zero."

        count = 0

        while a >= b:
            a = subtract(a, b)
            count += 1

        return str(count)

    return f"Unknown operation: {operation}"