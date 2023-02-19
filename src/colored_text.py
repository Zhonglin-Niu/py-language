# set color
# \u001b[31m

# reset
# \u001b[0m

# \u001b[31m{text}\u001b[0m

"""
Black: \u001b[30m
Red: \u001b[31m
Green: \u001b[32m
Yellow: \u001b[33m
Blue: \u001b[34m
Magenta: \u001b[35m
Cyan: \u001b[36m
White: \u001b[37m
Reset: \u001b[0m
"""

def gr(ob: object) -> object:
    return f"\u001b[32m{ob}\u001b[0m"

# make it brighter
# add a ;1
# e.g. \u001b[30;1m


# any color int: 0-255
# \u001b[38;5;{int}m{text}\u001b[0m
# \u001b[38;5;12200mhi\u001b[0m
