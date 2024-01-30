from rest_framework import serializers
from JobHub.utils.consts import PHONE_FIELD_DEFAULT_PLACEHOLDER, PHONE_FIELD_DEFAULT_MASK, PHONE_FIELD_DEFAULT_LABEL
from JobHub.utils.validators import MaskValidator


class PhoneField(serializers.CharField):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.style = kwargs.get('style', {'placeholder': PHONE_FIELD_DEFAULT_PLACEHOLDER,
                                          'mask': PHONE_FIELD_DEFAULT_MASK})
        self.label = kwargs.get('label', PHONE_FIELD_DEFAULT_LABEL)

        if 'mask' in self.style:
            self.validators.append(MaskValidator(self.style['mask']))


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        min_length = kwargs.pop('min_length', 8)
        super().__init__(*args, **kwargs)
        self.min_length = min_length

