import re

def expand_implicit_attributes(data, rules):
    implicit_attributes = {}
    for attribute, rules in rules.items():
        for rule in rules:
            if '*' in attribute:
                implicit_attributes[attribute] = _expand_attribute(data, attribute)
    return implicit_attributes

def _expand_attribute(data, attribute):
    pattern = attribute.replace('.', r'\.').replace('*', '[^.]+')
    regex = re.compile(f'^{pattern}$')
    expanded = []
    for key in data.keys():
        if regex.match(key):
            expanded.append(key)
    return expanded