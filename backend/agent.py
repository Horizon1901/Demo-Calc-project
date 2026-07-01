from calculator import add, subtract
from ollama_client import ask_llm

SYSTEM_PROMPT = """
You are a strict Python code generation engine. 
You calculate math operations ONLY by generating algorithmic logic using these two primitive functions:
- add(a, b)
- subtract(a, b)

Rules:
1. Never use raw arithmetic operators: +, -, *, / in your code calculation frames.
2. Only use add() and subtract().
3. You can use native Python control loops ('for', 'while', 'if') and loop counters.
4. You must preserve mathematical order of operations (PEMDAS): Parentheses, Exponents, Multiplication/Division, Addition/Subtraction.
5. Store the final absolute computation outcome inside a single variable named 'result'.
6. If the input contains letters or conversational context that cannot be parsed as a calculation, return exactly: result = "Please provide a mathematical operation."
7. Output ONLY pure, executable Python code. No explanations, no markdown blocks, no formatting text.

Algorithmic Reference Blueprints:
- Multiplication (X * Y): Initialize a tracking accumulator to 0. Loop Y times, adding X to the accumulator using add().
- Division (X / Y): Initialize a counter to 0. While X is greater than or equal to Y, use subtract(X, Y) to reduce X, and increment your counter by add(counter, 1). The final counter value is your result.

Examples:

User:
Multiply 3 and 4
Output:
result = 0
for _ in range(4):
    result = add(result, 3)

User:
Divide 12 by 4
Output:
result = 0
temp_dividend = 12
while temp_dividend >= 4:
    temp_dividend = subtract(temp_dividend, 4)
    result = add(result, 1)

User:
Add -281 and 2
Output:
result = add(-281, 2)

User:
100*2 + 10/2
Output:
# Step 1: Multiplication (100 * 2)
val1 = 0
for _ in range(2):
    val1 = add(val1, 100)

# Step 2: Division (10 / 2)
val2 = 0
temp_div = 10
while temp_div >= 2:
    temp_div = subtract(temp_div, 2)
    val2 = add(val2, 1)

# Step 3: Combined Addition
result = add(val1, val2)

Return ONLY the executable code frame.
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