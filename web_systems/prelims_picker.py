import random

while True:
    print(random.randint(1, 70))
    if input("Press enter to roll again, or 'q' to quit: ") == 'q':
        break
