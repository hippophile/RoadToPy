# I break the expression into parts and by using a stack I group those parts into correct groups

def parentheses(str):
    stack = []
    
    tokens = str.split()

    for part in tokens:
        if part == ")":
            # we want the last 3 tokens from the stack ex: 2 + 3
            op2 = stack.pop()   # operand
            op = stack.pop()    # operator
            op1 = stack.pop()   

            new_part = f"({op1} {op} {op2})"  # group the last parts into one (with the right par)
            stack.append(new_part)
        else:
            stack.append(part)

    return stack[0]

str = "1 + 2 ) * 3 - 4 ) * 5 - 6 ) ) )"

print(parentheses(str))


