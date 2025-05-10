import random
import string

def generate_random_password():

    characters = string.ascii_letters + string.digits
    password = []

    for i in range(10):
        random_char = random.choice(characters)
        password.append(random_char)

    password = "".join(password)
    return password