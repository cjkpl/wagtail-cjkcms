from django.utils.text import slugify as django_slugify
from unidecode import unidecode


def custom_slugify(value):
    # Convert to ASCII characters
    ascii_value = unidecode(value)
    # Use Django's built-in slugify after converting to ASCII
    return django_slugify(ascii_value)
