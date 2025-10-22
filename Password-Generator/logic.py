import random
import string


def generate_password(length):
    if length <= 0:
        raise ValueError("Length must be positive.")
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters)for _ in range(length))
    return password