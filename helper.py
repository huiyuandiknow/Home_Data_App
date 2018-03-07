def num(s):
    try:
        return int(s)
    except ValueError:
        return None


def alphabet_position(letter):
    alpha = "abcdefghijklmnopqrstuvwxyz"
    low_letter = letter.lower()
    return alpha.find(low_letter)


def is_it_big(letter):
    big_alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return letter in big_alpha


def rotate(char, rot):
    alpha = "abcdefghijklmnopqrstuvwxyz"
    if is_it_big(char):
        low_char = char.lower()
        return alpha[(alphabet_position(low_char) + rot) % 26].upper()
    elif char in alpha:
        return alpha[(alphabet_position(char) + rot) % 26]
    else:
        return char


def enc(text, rot=12):
    res = ""
    for symb in text:
        res = res + rotate(symb, rot)
    return res


def dec(text, rot=12):
    res = ""
    for symb in text:
        res = res + rotate(symb, -rot)
    return res
