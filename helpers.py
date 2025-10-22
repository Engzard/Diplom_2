import string
import random

URL = 'https://qa-scooter.praktikum-services.ru'


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string