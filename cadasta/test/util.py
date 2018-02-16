import random
import string


STRING_LENGTH = 24

alphabet = string.ascii_lowercase + string.digits
for loser in 'l1o0':
    i = alphabet.index(loser)
    alphabet = alphabet[:i] + alphabet[i + 1:]


def byte_to_base32_chr(byte):
    return alphabet[byte & 31]


def random_string():
    rand_bytes = [random.randint(0, 0xFF) for i in range(STRING_LENGTH)]
    return ''.join(map(byte_to_base32_chr, rand_bytes))


def random_us_number():
    rand_digits = [str(random.randint(0, 9)) for i in range(7)]
    return '+1628' + ''.join(rand_digits)
