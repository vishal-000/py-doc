import random
print("password generator")

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@$%^&*().,?0123456789'

number = int(input('enter amount of passwords to generate: '))
length = int(input('enter the length of the passwords: '))

print("\nHere are your passwords: ")

for _ in range(number):
  password = ''
  for _ in range(length):
    password += random.choice(chars)
  
  print(password)