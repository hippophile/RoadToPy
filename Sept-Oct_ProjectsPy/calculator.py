# function with dictionary 
def calculator(a, b, op):
    operations = {
        '+': a + b,
        '-': a - b,
        '*': a * b,
        '/': "Error: Division by zero" if b == 0 else a / b
    }
    return operations.get(op, "Invalid operator")

result = float(input("Insert first number: "))

while True:
    op = input("Insert the operator (+, -, *, / or E to exit): ")
    if op == 'E':
        print("Program Ended.")
        break

    b = float(input("Insert second number: "))

    # to make continuning operations
    result = calculator(result, b, op)

    print("Result:", result)