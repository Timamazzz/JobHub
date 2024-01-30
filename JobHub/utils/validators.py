import re
from rest_framework.exceptions import ValidationError


class MaskValidator:
    def __init__(self, regex=None):
        self.regex = regex

    def __call__(self, value):

        if not self.regex:
            return

        phone_pattern = re.compile(self.regex)
        if not phone_pattern.match(value):
            raise ValidationError(f"Invalid phone number format.")

