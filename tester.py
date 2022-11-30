from main import compute25
from cases import solutions

if __name__ == "__main__":
    for digits, solution in solutions.items():
        # print("Test case for", digits)
        expected = solution
        actual = compute25(digits)
        if (expected == "SIN SOLUCIÓN" or actual == "SIN SOLUCIÓN") and expected != actual:
            print("Expected:", expected)
            print("Actual:", actual)
            print("Test failed") 
            print()
