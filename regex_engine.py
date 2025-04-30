import re

def matcher(input_line, pattern):
    ptr1 = 0
    ptr2 = 0
    if input_line == "" and pattern == "":
        return True
    elif input_line == "":
        return False
    elif pattern == "":
        return True
    while ptr1 < len(input_line):
        if ptr2 + 1 < len(pattern) and pattern[ptr2] == "." and pattern[ptr2 + 1] == "+":
            if ptr1 >= len(input_line):
                return False
            ptr1 += 1
            while ptr1 < len(input_line):
                if matcher(input_line[ptr1:], pattern[ptr2 + 2:]):
                    return True
                ptr1 += 1
            return False
        if len(pattern) >= 2 and pattern[1] == '+':
            char_to_match = pattern[0]
            if input_line == "" or input_line[0] != char_to_match:
                return False
            i = 0
            while i < len(input_line) and input_line[i] == char_to_match:
                if matcher(input_line[i + 1:], pattern[2:]):
                    return True
                i += 1
            return matcher(input_line[i:], pattern[2:])
        if ptr2 + 1 < len(pattern) and pattern[ptr2 : ptr2 + 2] == "\\d":
            if input_line[ptr1].isdigit():
                return matcher(input_line[ptr1 + 1 :], pattern[ptr2 + 2 :])
            else:
                ptr1 = ptr1 + 1
        elif ptr2 + 1 < len(pattern) and pattern[ptr2 : ptr2 + 2] == "\\w":
            if input_line[ptr1].isalnum():
                return matcher(input_line[ptr1 + 1 :], pattern[ptr2 + 2 :])
            else:
                ptr1 = ptr1 + 1
        elif ptr2 + 1 < len(pattern) and pattern[ptr2 : ptr2 + 2] == "+":
            char_to_match = pattern[0]
            count = 0
            while count < len(input_line) and input_line[count] == char_to_match:
                count += 1
            if count == 0:
                return False  
            return matcher(input_line[count:], pattern[2:]) 
        elif ptr2 + 1 < len(pattern) and pattern[ptr2 + 1] == "?":
            if ptr1 < len(input_line) and input_line[ptr1] == pattern[ptr2]:
                return matcher(input_line[ptr1 + 1 :], pattern[ptr2 + 2 :])
            else:
                return matcher(input_line[ptr1:], pattern[ptr2 + 2 :])
        if pattern[ptr2] == ".":
            return matcher(input_line[ptr1 + 1:], pattern[ptr2 + 1:])
        elif input_line[ptr1] == pattern[ptr2]:
            return matcher(input_line[ptr1 + 1 :], pattern[ptr2 + 1 :])
        else:
            ptr1 = ptr1 + 1
    return False



def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        return pattern in input_line
    elif pattern == "\\d":
        for i in range(10):
            if input_line.find(str(i)) != -1:
                return True
    elif pattern == "\\w":
        return input_line.isalnum()
    elif pattern[0] == "^":
        if pattern[1] == input_line[0]:
            return [c in input_line for c in pattern[1:]]
        return False
    elif pattern[-1] == "$":
        if pattern[-2] == input_line[-1]:
            return [c in input_line for c in pattern[:-1]]
        return False
    elif pattern.startswith("[^") and pattern.endswith("]"):
        exclude_chars = set(pattern[2:-1])
        for ch in input_line:
            if ch not in exclude_chars:
                return True
        return False
    elif pattern[0] == "[" and pattern[-1] == "]":
        pat = pattern[1:-1]
        for c in input_line:
            if c in pattern[1:-1]:
                return True
    elif "(" in pattern and "|" in pattern and ")" in pattern:
        start = pattern.index("(")
        end = pattern.index(")")
        options = pattern[start + 1:end].split("|")

        for option in options:
            new_pattern = pattern[:start] + option + pattern[end + 1:]
            if match_pattern(input_line, new_pattern):
                return True
        return False
    elif pattern[-1] == "?":
        if pattern in input_line:
            return True
        return False
    else:
        return matcher(input_line, pattern)


