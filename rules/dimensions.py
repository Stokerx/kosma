from PIL import Image
from . import Rule

class Dimensions(Rule):
    def __init__(self, width=None, height=None, min_width=None, max_width=None, min_height=None, max_height=None, ratio=None):
        self.width = width
        self.height = height
        self.min_width = min_width
        self.max_width = max_width
        self.min_height = min_height
        self.max_height = max_height
        self.ratio = ratio

    def passes(self, attribute, value, parameters, validator):
        try:
            with Image.open(value) as img:
                width, height = img.size

                if self.width and width != self.width:
                    return False
                if self.height and height != self.height:
                    return False
                if self.min_width and width < self.min_width:
                    return False
                if self.max_width and width > self.max_width:
                    return False
                if self.min_height and height < self.min_height:
                    return False
                if self.max_height and height > self.max_height:
                    return False
                if self.ratio and round(width / height, 2) != round(self.ratio, 2):
                    return False

                return True
        except Exception:
            return False

    def message(self, attribute, value, parameters, validator):
        constraints = []
        if self.width:
            constraints.append(f"width={self.width}")
        if self.height:
            constraints.append(f"height={self.height}")
        if self.min_width:
            constraints.append(f"min_width={self.min_width}")
        if self.max_width:
            constraints.append(f"max_width={self.max_width}")
        if self.min_height:
            constraints.append(f"min_height={self.min_height}")
        if self.max_height:
            constraints.append(f"max_height={self.max_height}")
        if self.ratio:
            constraints.append(f"ratio={self.ratio}")

        return f"The {attribute} has invalid image dimensions. Required dimensions are: {', '.join(constraints)}."