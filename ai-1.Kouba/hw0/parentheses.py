def parentheses(str):
    stack01 = []
    stack02 = []
    
    tokens = str.split()

    for parts in tokens:
        stack01.append(parts)