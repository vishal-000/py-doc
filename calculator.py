import math

a = int(input("Enter a number : "))
b = int(input("Enter a number : "))
operator = input("Enter the operator : ")

if operator == '+':
    print(a+b)
if operator == '-':
    print(a-b)    
if operator == '*':
    print(a*b)
elif operator == '/':
    if b!= 0:
        print(a/b)
    else:
        print("Answer is not defined")
elif operator == 'sqrt':
    print("square root of a:", math.sqrt(a))
    print("square root of b:", math.sqrt(b))

else:
    print("Invalid operator")       