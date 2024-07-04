from django.core.exceptions import ValidationError
import re


def validate_passport(value):
    pattern = re.compile(r'^\d{4}-\d{6}$')
    if not pattern.match(value):
        raise ValidationError('Паспортные данные должны быть в формате "серия (4 цифры) - номер (6 цифр)"')
