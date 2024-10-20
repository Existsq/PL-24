import time
from contextlib import contextmanager

@contextmanager
def cm_timer_2():
    start_time = time.time()
    yield
    print(f"time: {time.time() - start_time:.3f}")

if __name__ == "__main__":
    with cm_timer_2():
        time.sleep(5.5)