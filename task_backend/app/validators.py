from django.contrib.auth.password_validation import PasswordValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomArgon2PasswordValidator(PasswordValidator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_password_hasher('django.contrib.auth.hashers.Argon2PasswordHasher')

    def validate(self, password, user=None):
        super().validate(password, user)
        if len(password) < 8:
            raise ValidationError(
                _("Пароль должен содержать как минимум 8 символов."),
                code='password_too_short',
            )
        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            raise ValidationError(
                _("Пароль должен содержать как буквы, так и цифры."),
                code='password_no_letters_or_digits',
            )

    def get_help_text(self):
        return _('Ваш пароль должен быть сложным и безопасным.')