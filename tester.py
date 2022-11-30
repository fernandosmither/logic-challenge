from main import compute25
from cases import solutions

if __name__ == "__main__":
    for digits, solution in solutions.items():
        print("Test case for", digits)
        expected = solution
        actual = compute25(digits)
        if expected == "SIN SOLUCIÓN"
        print("Expected:", solution)
        print("Actual:", compute25(digits))
        print()
