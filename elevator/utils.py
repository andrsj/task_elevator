# Additional functionality
# Small helping functions
from random import choice


def get_another_flour(flour_count: int, current_flour: int) -> int:
    values = list(range(1, flour_count + 1))
    if current_flour not in values:
        raise ValueError("Current flour too high! [{}] < [{}]".format(flour_count, current_flour))
    values.remove(current_flour)
    return choice(values)
