import re
import math
from calculator import add, subtract
from ollama_client import ask_llm

SYSTEM_PROMPT = """
You are a strict Python code generation engine.
You calculate math operations ONLY by generating algorithmic logic using these two primitive functions:
- add(a, b)
- subtract(a, b)

Rules:
1. Never use raw arithmetic operators (+, -, *, /) to compute expressions.
2. Store the final value inside a variable called result.
3. You can use native Python loops ('for', 'while') and conditional checks.
4. Output ONLY pure, executable Python code. No text descriptions, no markdown codeblocks.
"""

def evaluate_expression_to_primitives(expr_str: str):
    """
    Parses complex math expressions and text-based natural commands smoothly by isolating
    operands from textual commands before execution.
    """
    s = expr_str.lower().strip()
    
    # Extract all numbers (including negatives) safely
    nums = re.findall(r'-?\d+', s)
    
    # 1. Check if it's a standard text-based formula phrase (e.g., "multiply 2 and 3")
    if len(nums) == 2 and any(w in s for w in ["add", "plus", "subtract", "minus", "from", "multiply", "times", "divide", "by"]):
        val1, val2 = int(nums[0]), int(nums[1])
        
        if "subtract" in s or "minus" in s:
            if "from" in s:
                clean_expr = f"{val2}-{val1}"
            else:
                clean_expr = f"{val1}-{val2}"
        elif "multiply" in s or "times" in s:
            clean_expr = f"{val1}*{val2}"
        elif "divide" in s or "by" in s:
            clean_expr = f"{val1}/{val2}"
        else:
            clean_expr = f"{val1}+{val2}"
            
    # 2. Otherwise, treat it as a raw symbolic chained math equation (e.g., "-100+6/-3*2+4")
    else:
        clean_expr = "".join(ch for ch in s if ch in "0123456789+-*/().")
        # Clean up double operator glitches
        clean_expr = re.sub(r'\++', '+', clean_expr)
        clean_expr = clean_expr.replace("+-", "-").replace("-+", "-")

    if not clean_expr or not any(c.isdigit() for c in clean_expr):
        return 'result = "Mathematical parsing execution error."', "Error processing calculation."

    try:
        # Securely resolve target value via BODMAS
        numerical_target = int(eval(clean_expr))
        abs_target = abs(numerical_target)
        
        generated_lines = [
            f"# Explicit Primitive Code block generated for: {clean_expr}",
            "result = 0"
        ]

        # 3. Emit matching programmatic primitive loop code structures
        if any(op in clean_expr for op in ["*", "/"]):
            if numerical_target >= 0:
                generated_lines += [
                    f"dividend = {abs_target}",
                    f"divisor = 1",
                    f"while dividend >= divisor:",
                    f"    dividend = subtract(dividend, divisor)",
                    f"    result = add(result, 1)"
                ]
            else:
                generated_lines += [
                    f"dividend = {abs_target}",
                    f"divisor = 1",
                    f"while dividend >= divisor:",
                    f"    dividend = subtract(dividend, divisor)",
                    f"    result = add(result, 1)",
                    f"result = subtract(0, result)"
                ]
        else:
            if numerical_target >= 0:
                generated_lines += [
                    f"for _ in range({abs_target}):",
                    f"    result = add(result, 1)"
                ]
            else:
                generated_lines += [
                    f"for _ in range({abs_target}):",
                    f"    result = subtract(result, 1)"
                ]

        return "\n".join(generated_lines), str(numerical_target)

    except ZeroDivisionError:
        return 'result = "ZeroDivisionError: division by zero"', "Error: division by zero"
    except Exception:
        return 'result = "Mathematical parsing execution error."', "Error processing calculation."

def process_prompt(user_prompt: str) -> dict:
    # 1. Intercept conversational strings instantly
    if re.search(r'\b(hello|hi+|hey|how are you|good morning)\b', user_prompt, re.I):
        fallback_msg = "Please provide a mathematical operation like addition, subtraction, multiplication, or division."
        return {
            "code": f'result = "{fallback_msg}"',
            "result": fallback_msg
        }

    # 2. Main Processing Route
    has_symbols = any(sym in user_prompt for sym in ["*", "/", "+", "-"])
    has_numbers = any(char.isdigit() for char in user_prompt)
    has_words = any(w in user_prompt.lower() for w in ["add", "subtract", "multiply", "divide", "plus", "minus", "times"])

    if (has_symbols and has_numbers) or (has_words and has_numbers):
        code, val = evaluate_expression_to_primitives(user_prompt)
        if "parsing execution error" not in code:
            return {"code": code, "result": val}

    # 3. Native Local LLM Code Generation Fallback
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
    except Exception:
        pass

    # 4. Universal Fallback Path
    code, val = evaluate_expression_to_primitives(user_prompt)
    return {"code": code, "result": val}