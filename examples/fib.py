from functools import cache as кэш


@кэш
def фибоначчи(номер):
    if номер == 0:
        return 0
    if номер in [1, 2]:
        return 1
    return фибоначчи(номер - 1) + фибоначчи(номер - 2)
