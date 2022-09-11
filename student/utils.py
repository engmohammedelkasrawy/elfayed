import random

def random_digits(n):
    return int(''.join([str(random.randint(0, 10)) for _ in range(n)]))
