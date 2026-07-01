from calculator import add, subtract
from ollama_client import ask_llm

SYSTEM_PROMPT = """
You are a Python code generation engine.

You ONLY have access to these functions:

add(a, b)
subtract(a, b)

Rules:

1. Never use +, -, * or / operators.
2. Never define new functions.
3. Only use add() and subtract().
4. Store the final answer in a variable called result.
5. Return ONLY executable Python code.
6. Do not explain anything.
7. Do not use markdown.
8. Do not use ```python.

Examples:

User:
Add 2 and 3

Output:

result = add(2, 3)

-----------------------------------

User:
Subtract 10 and 4

Output:

result = subtract(10, 4)

-----------------------------------

User:
Multiply 2 by 3

Output:

result = 0

for _ in range(3):
    result = add(result, 2)

-----------------------------------

User:
Multiply 5 by 4

Output:

result = 0

for _ in range(4):
    result = add(result, 5)

-----------------------------------

User:
Divide 8 by 2

Output:

result = 0
count = 0

while result != 8:
    result = add(result, 2)
    count = add(count, 1)

result = count

Return ONLY the Python code.
"""


def process_prompt(user_prompt: str):

    # Ask the LLM to generate Python code
    generated_code = ask_llm(
        SYSTEM_PROMPT,
        user_prompt
    )
    generated_code = generated_code.replace("```python", "")
    generated_code = generated_code.replace("```", "")
    generated_code = generated_code.strip()

    print("\n========== GENERATED CODE ==========")
    print(generated_code)
    print("====================================\n")

    # Only expose these functions and necessary iterators to the generated code
    safe_globals = {
        "add": add,
        "subtract": subtract,
        "__builtins__": {
            "range": range
        }
    }

    safe_locals = {}

    try:
        exec(generated_code, safe_globals, safe_locals)
    except Exception as e:
        return {
            "code": generated_code,
            "result": f"Execution Error:\n{e}"
        }

    if "result" not in safe_locals:
        return {
            "code": generated_code,
            "result": "The generated code did not produce a variable named 'result'."
        }

    return {
        "code": generated_code,
        "result": str(safe_locals["result"])
    }