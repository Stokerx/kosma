import re
from . import Rule

class Password(Rule):
    def __init__(self, min_length=None, letters=False, mixed_case=False, numbers=False, symbols=False, uncompromised=False):
        self.min_length = min_length
        self.letters = letters
        self.mixed_case = mixed_case
        self.numbers = numbers
        self.symbols = symbols
        self.uncompromised = uncompromised

    def passes(self, attribute, value, parameters, validator):
        if self.min_length and len(value) < self.min_length:
            return False
        if self.letters and not re.search(r"[a-zA-Z]", value):
            return False
        if self.mixed_case and not (re.search(r"[a-z]", value) and re.search(r"[A-Z]", value)):
            return False
        if self.numbers and not re.search(r"\d", value):
            return False
        if self.symbols and not re.search(r"[^a-zA-Z0-9\s]", value):
            return False
        if self.uncompromised:
            # Aquí se puede integrar la lógica para verificar contraseñas comprometidas
            pass
        return True

    def message(self, attribute, value, parameters, validator):
        messages = []
        if self.min_length:
            messages.append(f"at least {self.min_length} characters")
        if self.letters:
            messages.append("at least one letter")
        if self.mixed_case:
            messages.append("at least one uppercase and one lowercase letter")
        if self.numbers:
            messages.append("at least one number")
        if self.symbols:
            messages.append("at least one symbol")
        if self.uncompromised:
            messages.append("must not be compromised")
        
        message_str = f"The {attribute} must have " + ", ".join(messages) + "."
        return message_str