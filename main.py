

import sympy as sp


# Solvers


def solve_arithmetic(expr):
    try:
        parsed = sp.sympify(expr)
        steps = [f"Step 1: Parsed expression: {parsed}"]
        result = parsed.evalf()
        steps.append(f"Step 2: Evaluated result: {result}")
        return "\n".join(steps)
    except Exception as e:
        return f"Error: {e}"

def solve_equation(eq_str):
    try:
        x = sp.Symbol('x')
        left, right = eq_str.split('=')
        left_expr = sp.sympify(left)
        right_expr = sp.sympify(right)
        eq = sp.Eq(left_expr, right_expr)

        steps = [f"Step 1: Start with the equation: {eq}"]

        combined = left_expr - right_expr
        steps.append(f"Step 2: Move all terms to one side: {combined} = 0")

        sol = sp.solve(eq, x)

        if isinstance(left_expr, sp.Add) or isinstance(left_expr, sp.Mul) or left_expr.has(x):
            poly = sp.Poly(combined, x)
            a = poly.coeff_monomial(x)
            b = poly.coeff_monomial(1)
            if a != 0:
                steps.append(f"Step 3: Rearranged as: {a}*x + {b} = 0")
                steps.append(f"Step 4: Subtract {b} from both sides: {a}*x = {-b}")
                steps.append(f"Step 5: Divide both sides by {a}: x = {-b}/{a}")
                steps.append(f"Step 6: Solution: x = {sol[0]}")
            else:
                steps.append(f"Step 3: No x term detected. Solution: x = {sol[0]}")
        else:
            steps.append(f"Step 3: Solution: x = {sol[0]}")

        return "\n".join(steps)
    except Exception as e:
        return f"Error: {e}"

def solve_quadratic(eq_str):
    try:
        x = sp.Symbol('x')
        left, right = eq_str.split('=')
        left_expr = sp.sympify(left)
        right_expr = sp.sympify(right)
        eq = sp.Eq(left_expr, right_expr)

        poly = sp.Poly(left_expr - right_expr, x)
        a, b, c = poly.all_coeffs()

        steps = [f"Step 1: Equation: {eq}"]
        steps.append(f"Step 2: Identify coefficients: a = {a}, b = {b}, c = {c}")
        discriminant = b**2 - 4*a*c
        steps.append(f"Step 3: Compute discriminant: D = b² - 4ac = {discriminant}")

        if discriminant > 0:
            steps.append("Step 4: Two real roots exist")
        elif discriminant == 0:
            steps.append("Step 4: One real root exists")
        else:
            steps.append("Step 4: Complex roots exist")

        sqrt_disc = sp.sqrt(discriminant)
        sol1 = (-b + sqrt_disc) / (2*a)
        sol2 = (-b - sqrt_disc) / (2*a)
        steps.append("Step 5: Use quadratic formula:")
        steps.append(f"x = (-b ± √D) / 2a = ({-b} ± √{discriminant}) / {2*a}")
        steps.append(f"Step 6: Solutions: x = {sol1}, x = {sol2}")

        return "\n".join(steps)
    except Exception as e:
        return f"Error: {e}"

def simplify_expression(expr):
    try:
        simp = sp.simplify(sp.sympify(expr))
        return f"Simplified Expression: {simp}"
    except Exception as e:
        return f"Error: {e}"

def differentiate(expr):
    import re
    expr = re.sub(r"\be\b", "E", expr)
    if(expr == "E**x"):
        return "e**x"
    try:
        x = sp.Symbol('x')
        parsed = sp.sympify(expr)
        deriv = sp.diff(parsed, x)
        steps = [f"Step 1: Parsed expression: {parsed}", f"Step 2: Differentiate w.r.t x: {deriv}"]
        return "\n".join(steps)
    except Exception as e:
        return f"Error: {e}"

def integrate(expr, lower=None, upper=None):
    try:
        x = sp.Symbol('x')
        parsed = sp.sympify(expr)

        steps = [f"Step 1: Parsed expression: {parsed}"]

        if lower is not None and upper is not None:
            result = sp.integrate(parsed, (x, float(lower), float(upper)))
            steps.append(f"Step 2: Definite integral from {lower} to {upper}")
            steps.append(f"Step 3: Result: {result}")
        else:
            result = sp.integrate(parsed, x)
            steps.append(f"Step 2: Indefinite integral w.r.t x: {result} + C")

        return "\n".join(steps)
    except Exception as e:
        return f"Error: {e}"


def solve_simultaneous(eq1, eq2):
    try:
        x, y = sp.symbols('x y')
        e1 = sp.Eq(*map(sp.sympify, eq1.split('=')))
        e2 = sp.Eq(*map(sp.sympify, eq2.split('=')))
        steps = [f"Step 1: First equation: {e1}", f"Step 2: Second equation: {e2}"]
        sol = sp.solve((e1, e2), (x, y))
        steps.append(f"Step 3: Solved values: {sol}")
        return "\n".join(steps)
    except Exception as e:
        return f"Error: {e}"


# Dispatcher (used by Mistral)


def dispatch_problem(problem):
    try:
        ptype = problem.get("type")
        expr = problem.get("expr")

        if ptype == "arithmetic":
            return solve_arithmetic(expr)
        elif ptype == "equation_1var":
            return solve_equation(expr)
        elif ptype == "quadratic":
            return solve_quadratic(expr)
        elif ptype == "simplify":
            return simplify_expression(expr)
        elif ptype == "differentiate":
            return differentiate(expr)
        elif ptype == "integrate":
            return integrate(expr)
        elif ptype == "simultaneous" and isinstance(expr, list) and len(expr) == 2:
            return solve_simultaneous(expr[0], expr[1])
        else:
            return "Unsupported problem type or invalid input."
    except Exception as e:
        return f"Error in dispatch: {e}"

# Simulated Mistral NLP interpreter


import requests
import json

def mistral_interpret(question):

    # This is the Training Data. There are 48 entries.

    prompt = f"""

    
    You are a math interpreter bot. Your job is to convert any kind of math question into a valid symbolic expression, and categorize it by type.

    Your output must be only a JSON object with this format:

    {{
    "type": "arithmetic" | "equation_1var" | "quadratic" | "simplify" | "differentiate" | "integrate" | "simultaneous",
    "expr": string or list of strings (equations),
    "variables": [list of variable names, optional]
    }}

    --- EXAMPLES ---

    Q1: I had 8 candies, I ate 3. How many are left?  
    A1:
    {{
    "type": "arithmetic",
    "expr": "8 - 3"
    }}

    Q2: My brother has 4 apples. I give him 6 more. How many apples does he have now?  
    A2:
    {{
    "type": "arithmetic",
    "expr": "4 + 6"
    }}

    Q3: Convert 3 hours into minutes.  
    A3:
    {{
    "type": "arithmetic",
    "expr": "3 * 60"
    }}

    Q4: A car travels 180 km in 3 hours. What is its average speed?  
    A4:
    {{
    "type": "arithmetic",
    "expr": "180 / 3"
    }}

    Q5: A man buys 5 pens for ₹100. What is the cost of one pen?  
    A5:
    {{
    "type": "arithmetic",
    "expr": "100 / 5"
    }}

    Q6: Solve: 3x - 9 = 0  
    A6:
    {{
    "type": "equation_1var",
    "expr": "3*x - 9 = 0",
    "variables": ["x"]
    }}

    Q7: Two more than twice a number is equal to 10. Find the number.  
    A7:
    {{
    "type": "equation_1var",
    "expr": "2*x + 2 = 10",
    "variables": ["x"]
    }}

    Q8: The sum of a number and its square is 30.  
    A8:
    {{
    "type": "quadratic",
    "expr": "x**2 + x = 30",
    "variables": ["x"]
    }}

    Q9: Solve: x² - 4x + 4 = 0  
    A9:
    {{
    "type": "quadratic",
    "expr": "x**2 - 4*x + 4 = 0",
    "variables": ["x"]
    }}

    Q10: Simplify (x² - 1)/(x - 1)  
    A10:
    {{
    "type": "simplify",
    "expr": "(x**2 - 1)/(x - 1)",
    "variables": ["x"]
    }}

    Q11: Differentiate x² * sin(x)  
    A11:
    {{
    "type": "differentiate",
    "expr": "x**2 * sin(x)",
    "variables": ["x"]
    }}

    Q12: Integrate 1 / (1 + x²)  
    A12:
    {{
    "type": "integrate",
    "expr": "1 / (1 + x**2)",
    "variables": ["x"]
    }}

    Q13: Solve the system:  
    x + y = 10  
    x - y = 2  
    A13:
    {{
    "type": "simultaneous",
    "expr": ["x + y = 10", "x - y = 2"],
    "variables": ["x", "y"]
    }}

    Q14: If angle A and angle B are complementary and angle A = 40°, what is angle B?  
    A14:
    {{
    "type": "arithmetic",
    "expr": "90 - 40"
    }}

    Q15: Find the perimeter of a square with side length 12  
    A15:
    {{
    "type": "arithmetic",
    "expr": "4 * 12"
    }}

    Q16: I walk 3 km in 30 minutes. What is my speed in km/hr?  
    A16:
    {{
    "type": "arithmetic",
    "expr": "3 / (30 / 60)"
    }}

    Q17: Half of a number is 15. Find the number.  
    A17:
    {{
    "type": "equation_1var",
    "expr": "x / 2 = 15",
    "variables": ["x"]
    }}

    Q18: The product of a number and 6 is 54.  
    A18:
    {{
    "type": "equation_1var",
    "expr": "6*x = 54",
    "variables": ["x"]
    }}

    Q19: A tank fills with 20 liters every 5 minutes. How many liters in 1 hour?  
    A19:
    {{
    "type": "arithmetic",
    "expr": "(60 / 5) * 20"
    }}

    Q20: The square of a number is 49  
    A20:
    {{
    "type": "equation_1var",
    "expr": "x**2 = 49",
    "variables": ["x"]
    }}

    ### Basic Arithmetic
    Q: What is 5 plus 3 times 2?
    A: {{"type": "arithmetic", "expr": "5 + 3 * 2"}}

    Q: I had 10 chocolates and ate 4. How many left?
    A: {{"type": "arithmetic", "expr": "10 - 4"}}

    Q: A pen costs ₹15. How much for 5 pens?
    A: {{"type": "arithmetic", "expr": "15 * 5"}}

    Q: Convert 2.5 hours into minutes
    A: {{"type": "arithmetic", "expr": "2.5 * 60"}}

    Q: A car travels 120 km in 3 hours. What's the speed?
    A: {{"type": "arithmetic", "expr": "120 / 3"}}

    ### Algebra – One Variable
    Q: Solve 2x + 3 = 9
    A: {{"type": "equation_1var", "expr": "2*x + 3 = 9", "variables": ["x"]}}

    Q: Three times a number minus 5 equals 7
    A: {{"type": "equation_1var", "expr": "3*x - 5 = 7", "variables": ["x"]}}

    Q: Half of a number plus 4 is 10
    A: {{"type": "equation_1var", "expr": "x/2 + 4 = 10", "variables": ["x"]}}

    ### Quadratic Equations
    Q: x squared minus 5x plus 6 equals 0
    A: {{"type": "quadratic", "expr": "x**2 - 5*x + 6 = 0", "variables": ["x"]}}

    Q: The square of a number plus 2 equals 35
    A: {{"type": "quadratic", "expr": "x**2 + 2 = 35", "variables": ["x"]}}

    Q: The product of two consecutive integers is 56
    A: {{"type": "quadratic", "expr": "x*(x + 1) = 56", "variables": ["x"]}}

    ### Simplification
    Q: Simplify (x² + 2x + 1)/(x + 1)
    A: {{"type": "simplify", "expr": "(x**2 + 2*x + 1)/(x + 1)", "variables": ["x"]}}

    Q: Simplify (a² - b²)/(a - b)
    A: {{"type": "simplify", "expr": "(a**2 - b**2)/(a - b)", "variables": ["a", "b"]}}

    ### Calculus – Differentiation
    Q: What is the derivative of x squared times sin x?
    A: {{"type": "differentiate", "expr": "x**2 * sin(x)", "variables": ["x"]}}

    Q: Differentiate x³ + 3x² - 4x
    A: {{"type": "differentiate", "expr": "x**3 + 3*x**2 - 4*x", "variables": ["x"]}}

    ### Calculus – Integration
    Q: Integrate 1 / (1 + x²)
    A: {{"type": "integrate", "expr": "1 / (1 + x**2)", "variables": ["x"]}}

    Q: Find ∫x·e^x dx
    A: {{"type": "integrate", "expr": "x*exp(x)", "variables": ["x"]}}

    Q: Integrate sin(x) from 0 to π
    A: {{"type": "integrate", "expr": "sin(x)", "variables": ["x"]}}

    ### Simultaneous Equations
    Q: Solve x + y = 4 and x - y = 2
    A: {{"type": "simultaneous", "expr": ["x + y = 4", "x - y = 2"], "variables": ["x", "y"]}}

    Q: Solve: 2x + 3y = 12, 4x - y = 5
    A: {{"type": "simultaneous", "expr": ["2*x + 3*y = 12", "4*x - y = 5"], "variables": ["x", "y"]}}

    ### Physics – Motion
    Q: A body starts with velocity 2 m/s and accelerates at 9.8 m/s² for 2 seconds. What is its final velocity?
    A: {{"type": "physics", "expr": "2 + 9.8 * 2"}}

    Q: A body falls freely under gravity for 3 seconds. Find its speed (u = 0)
    A: {{"type": "physics", "expr": "0 + 9.8 * 3"}}

    Q: Find distance travelled by object accelerating at 5 m/s² for 4s from rest
    A: {{"type": "physics", "expr": "0.5 * 5 * 4**2"}}

    Q: A car decelerates from 20 m/s to 0 in 4s. What is the acceleration?
    A: {{"type": "physics", "expr": "(0 - 20) / 4"}}

    ### Geometry
    Q: What is the area of a circle with radius 7?
    A: {{"type": "arithmetic", "expr": "pi * 7**2"}}

    Q: A square has side 12 cm. Find its perimeter
    A: {{"type": "arithmetic", "expr": "4 * 12"}}

    Q: A triangle has base 10 cm and height 5 cm. Find its area.
    A: {{"type": "arithmetic", "expr": "0.5 * 10 * 5"}}

    

    ---

    Now process this question:
    {question}
    """
    # There are 48 entries.



    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )
        content = response.json()['response'].strip()

        # Ensure only JSON is extracted
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        json_str = content[json_start:json_end]

        return json.loads(json_str)
    except Exception as e:
        return {"type": "error", "expr": f"Failed to parse: {e}"}



# Mistral-Driven Mode


def interactive_mode():
    print("\n=== Natural Language Math Solver (Mistral Mode) ===")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nAsk your math question: ")
        if question.lower() == 'exit':
            break
        problem = mistral_interpret(question)
        if not problem:
            print("Sorry, Mistral could not interpret the input.")
            continue
        result = dispatch_problem(problem)
        print("\n" + result)


# Main menu for manual mode (optional)


def main():
    print("\n=== Math Solver Bot ===")
    print("1. Interactive (Mistral-driven)")
    print("2. Manual mode (CLI options)")
    print("0. Exit")

    while True:
        choice = input("\nChoose mode (0–2): ")
        if choice == '0':
            print("Goodbye!")
            break
        elif choice == '1':
            interactive_mode()
        elif choice == '2':
            print("\nManual Mode:")
            print("1. Arithmetic")
            print("2. Equation in 1 variable")
            print("3. Quadratic")
            print("4. Simplify")
            print("5. Differentiate")
            print("6. Integrate")
            print("7. Simultaneous Equations (2 vars)")

            sub_choice = input("Choose (1–7): ")

            if sub_choice == '1':
                expr = input("Enter arithmetic expression: ")
                print(solve_arithmetic(expr))
            elif sub_choice == '2':
                eq = input("Enter linear equation (e.g., 2*x + 3 = 7): ")
                print(solve_equation(eq))
            elif sub_choice == '3':
                eq = input("Enter quadratic equation (e.g., x**2 + 5*x + 6 = 0): ")
                print(solve_quadratic(eq))
            elif sub_choice == '4':
                expr = input("Enter expression to simplify: ")
                print(simplify_expression(expr))
            elif sub_choice == '5':
                expr = input("Enter expression to differentiate (in x): ")
                print(differentiate(expr))
            elif sub_choice == '6':
                expr = input("Enter expression to integrate (in x): ")
                print(integrate(expr))
            elif sub_choice == '7':
                eq1 = input("Enter 1st equation (e.g., x + y = 4): ")
                eq2 = input("Enter 2nd equation (e.g., x - y = 2): ")
                print(solve_simultaneous(eq1, eq2))
            else:
                print("Invalid sub-choice.")
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
