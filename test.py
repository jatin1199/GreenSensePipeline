def give_output(n):
    if n <= 1:
        return n
    else:
        return give_output(n-1) + give_output(n-2)