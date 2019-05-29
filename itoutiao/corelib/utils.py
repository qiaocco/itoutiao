def is_numeric(value):
    try:
        int(value)
    except (ValueError, TypeError):
        return False
    return True


def trunc_utf8(string, num, etc="..."):
    if num > len(string):
        return string

    if etc:
        trunc_idx = num - len(etc)
    else:
        trunc_idx = num
    ret = string[:trunc_idx]
    if etc:
        ret += etc
    return ret
