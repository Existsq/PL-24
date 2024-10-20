import json
from random import randint
from contextlib import contextmanager


@contextmanager
def cm_timer_1():
    import time
    start_time = time.time()
    yield
    print(f"time: {time.time() - start_time:.3f}")


def print_result(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(func.__name__)
        if isinstance(result, list):
            print(*result, sep='\n')
        elif isinstance(result, dict):
            for key, value in result.items():
                print(f"{key} = {value}")
        else:
            print(result)
        return result

    return wrapper


@print_result
def f1(data):
    return sorted(set(job['job-name'].lower() for job in data))


@print_result
def f2(data):
    return list(filter(lambda x: x.lower().startswith("программист"), data))


@print_result
def f3(data):
    return list(map(lambda x: f"{x} с опытом Python", data))


@print_result
def f4(data):
    return list(map(lambda x: f"{x}, зарплата {randint(100000, 200000)} руб.", data))


if __name__ == "__main__":
    path = 'data_light.json'
    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    with cm_timer_1():
        f4(f3(f2(f1(data))))