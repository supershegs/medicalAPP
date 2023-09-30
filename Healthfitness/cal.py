from django.utils.crypto import get_random_string
print(int(get_random_string(12, allowed_chars='0123456789')))