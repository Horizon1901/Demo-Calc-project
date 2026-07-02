import re
from calculator import add, subtract
from ollama_client import ask_llm

SYSTEM_PROMPT = """
You are a strict Python code generation engine.
You calculate math operations ONLY by generating algorithmic logic using these two primitive functions:
- add(a, b)
- subtract(a, b)

Rules:
1. Never use raw arithmetic operators (+, -, *, /) or python's eval() to compute expressions.
2. Store the final value inside a variable called result.
3. You can use native Python loops ('for', 'while'), variables, and conditional checks.
4. Output ONLY pure, executable Python code. No text descriptions, no markdown codeblocks, no prose.
5. For multiplication, use a loop with add(). For division, use a loop with subtract(). Resolve negative signs carefully.
"""

def process_prompt(user_prompt: str) -> dict:
   
    if re.search(r'\b(hello|hi+|hey|how are you|good morning)\b', user_prompt, re.I):
        fallback_msg = "Please provide a mathematical operation like addition, subtraction, multiplication, or division."
        return {
            "code": f'result = "{fallback_msg}"',
            "result": fallback_msg
        }

    try:
        generated_code = ask_llm(SYSTEM_PROMPT, user_prompt)
 
        generated_code = re.sub(r'```python|```', '', generated_code).strip()

        safe_globals = {
            "add": add,
            "subtract": subtract,
            "__builtins__": {"range": range, "abs": abs, "int": int}
        }
        safe_locals = {}

        exec(generated_code, safe_globals, safe_locals)
        
        if "result" in safe_locals:
            return {
                "code": generated_code,
                "result": str(safe_locals["result"])
            }
            
    except Exception as exc:
        return {
            "code": f"# Execution error fallback\nresult = 'Error during LLM code execution: {exc}'",
            "result": f"Error parsing operation."
        }

    return {
        "code": "# Fallback block\nresult = 'Could not parse execution payload'",
        "result": "Error processing calculation."
    }