from . import Rule

class Mimetypes(Rule):
    def __init__(self, *allowed_types):
        self.allowed_types = allowed_types

    def passes(self, attribute, value, parameters, validator):
        if not hasattr(value, 'content_type'):
            return False
        return value.content_type in self.allowed_types

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be a file of type: {', '.join(self.allowed_types)}."