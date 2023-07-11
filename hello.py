import numpy as np


def hello():
    return ("Hello, world!")


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    if b == 0:
        raise ValueError("Can't divide by zero!")
    return a / b


def sqrt(a):
    return np.sqrt(a)


def power(a, b):
    return np.power(a, b)


def log(a):
    return np.log(a)


def exp(a):
    return np.exp(a)


def sin(a):
    return np.sin(a)


def cos(a):
    return np.cos(a)


def tan(a):
    return np.tan(a)


def cot(a):
    return 1 / np.tan(a)


def __main__():
    hello()


if __name__ == "__main__":
    __main__()
