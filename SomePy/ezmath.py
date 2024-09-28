print("To solve the ax+b=0 \n")

a = int(input("input the number a :"))

b = int(input("input the number b :"))

def mathez(a,b):
    if a == 0:
        return
    else:
        return -(b/a)

x = mathez(a,b)

if x is None:
    print("This equation has no solution...")
else:
    print("The solution of the equation (a)x+b=0 is", x)