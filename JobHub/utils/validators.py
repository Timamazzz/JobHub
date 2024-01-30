import re
from rest_framework.exceptions import ValidationError


class MaskValidator:
    def __init__(self, mask=None):
        self.mask = mask

    def __call__(self, value):

        if not self.mask:
            return

        phone_pattern = re.compile(self.mask)
        if not phone_pattern.match(value):
            raise ValidationError(f"Invalid phone number format.")

