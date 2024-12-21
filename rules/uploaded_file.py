import os
from . import Rule

class UploadedFile(Rule):
    def __init__(self, min_size=None, max_size=None, allowed_extensions=None):
        self.min_size = min_size  # Tamaño en KB
        self.max_size = max_size  # Tamaño en KB
        self.allowed_extensions = allowed_extensions

    def passes(self, attribute, value, parameters, validator):
        if not hasattr(value, 'path') or not hasattr(value, 'extension'):
            return False

        if not os.path.exists(value.path):
            return False

        file_size = os.path.getsize(value.path) / 1024  # Convertir bytes a KB

        if self.min_size is not None and file_size < self.min_size:
            return False

        if self.max_size is not None and file_size > self.max_size:
            return False

        if self.allowed_extensions:
            ext = value.extension.lower()
            if ext not in [e.lower() for e in self.allowed_extensions]:
                return False

        return True

    def message(self, attribute, value, parameters, validator):
        messages = []
        if self.min_size is not None:
            messages.append(f"min size: {self.min_size}KB")
        if self.max_size is not None:
            messages.append(f"max size: {self.max_size}KB")
        if self.allowed_extensions:
            messages.append(f"allowed extensions: {', '.join(self.allowed_extensions)}")
        return f"The {attribute} failed to pass file validation. Constraints: {', '.join(messages)}."