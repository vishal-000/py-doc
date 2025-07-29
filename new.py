def factorial(x):
    if x == 0 | x==1:
        return 1
    start = 1
    for i in range(2,x+1):
        start = start * i
    return start
number = int(input("Enter the number :"))
print("the factorial of", number ,"is", factorial(number))