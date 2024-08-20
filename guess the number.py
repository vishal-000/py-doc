import random

def guess(x):
    random_number = random.randint(0, x)
    guess = 0
    while guess != random_number :
        guess = int(input(f"guess the number between 0 and {x} :"))
        if guess > random_number :
            print("guess again.it is too high")
        elif guess < random_number :
            print("guess again.it is too low")

    print(f"you got the right number -'{random_number}'")
guess(10)