import functools

def repeat(n):
    def repeat_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return repeat_decorator


if __name__ == '__main__':
    @repeat(3)
    def myFunc():
        print('Hello World!')

    myFunc()