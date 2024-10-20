import time

class cm_timer_1:
    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"time: {time.time() - self.start_time:.3f}")

if __name__ == "__main__":
    with cm_timer_1():
        time.sleep(5.5)