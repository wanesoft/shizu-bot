import string
import random


def generate_hex_string(length=24):
    hex_chars = string.hexdigits
    return ''.join(random.choice(hex_chars).lower() for _ in range(length))