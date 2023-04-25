import time
from typing import Any, Callable


def measure_time(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.4f}s")
        return result

    return wrapper
    