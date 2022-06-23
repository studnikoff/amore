def square(size):
    for i in range(size):
        print(i)
        yield i**2


if __name__ == '__main__':
    next(square(10))