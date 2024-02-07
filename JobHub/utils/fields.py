from rest_framework import serializers
from JobHub.utils.consts import PHONE_FIELD_DEFAULT_PLACEHOLDER, PHONE_FIELD_DEFAULT_MASK, PHONE_FIELD_DEFAULT_LABEL, \
    PHONE_FIELD_DEFAULT_REGEX
from JobHub.utils.validators import MaskValidator


def formate_phone(phone):
    digits_only = ''.join(filter(lambda x: x.isdigit(), phone))

    if len(digits_only) == 11 and digits_only.startswith('8'):
        digits_only = '+7' + digits_only[1:]

    formatted_phone = f'{digits_only[1:4]}{digits_only[4:7]}{digits_only[7:9]}{digits_only[9:]}'

    return formatted_phone


class PhoneField(serializers.CharField):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.style = kwargs.get('style', {'placeholder': PHONE_FIELD_DEFAULT_PLACEHOLDER,
                                          'mask': PHONE_FIELD_DEFAULT_MASK})
        self.label = kwargs.get('label', PHONE_FIELD_DEFAULT_LABEL)

        if 'mask' in self.style:
            self.regex = kwargs.get('regex', PHONE_FIELD_DEFAULT_REGEX)
            # self.validators.append(MaskValidator(regex=self.regex))


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        min_length = kwargs.pop('min_length', 8)
        super().__init__(*args, **kwargs)
        self.min_length = min_length
