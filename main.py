
import functools
import multiprocessing

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return functools.reduce(lambda x, _: (x[1], x[0] + x[1]), range(n-1), (0, 1))[1]

def factorial(n):
    if n == 0:
        return 1
    else:
        return functools.reduce(lambda x, y: x * y, range(1, n+1))

def create_large_list():
    return list(range(1000000))

