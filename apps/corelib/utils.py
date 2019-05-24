def is_numeric(value):
    try:
        int(value)
    except (ValueError, TypeError):
        return False
    return True
