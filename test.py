from copy import deepcopy


def reverse_digit(digit):
    return int(str(digit)[::-1])


if __name__ == "__main__":
    a = {1: 1, 2: 2, 3: 3, 4: {1: 1, 2: 2}}
    b = deepcopy(a)
    print(id(a.get(4)))
    print(id(b.get(4)))
