from . import Rule

class Image(Rule):
    def passes(self, attribute, value, parameters, validator):
        if not hasattr(value, 'content_type'):
            return False
        return value.content_type in ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/svg+xml', 'image/webp']

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be an image (jpeg, png, bmp, gif, svg, or webp)."