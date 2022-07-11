from functools import wraps
from time import time

def timer(round_digits=1):
    def timer_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time()
            result = func(*args, **kwargs)
            end_time = time()
            time_elapsed = end_time - start_time
            print(f'Function "{func.__name__}" executed in '
                  f'{round(time_elapsed, round_digits)} seconds.')
            return result
        return wrapper
    return timer_decorator


if __name__ == '__main__':
    @timer(2)
    def do_some_math():
        print('Demo process begun. Computing...')
        for i in range(8000):
            for j in range(8000):
                i+j

    do_some_math()