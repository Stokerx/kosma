import os
from decimal import Decimal, InvalidOperation

def get_size(attribute, value, parameters, validator):
    if isinstance(value, (int, float)):
        return value
    elif isinstance(value, str):
        return len(value)
    elif isinstance(value, list):
        return len(value)
    elif hasattr(value, 'size'):
        return value.size / 1024  # Assuming size attribute returns bytes
    else:
        return 0