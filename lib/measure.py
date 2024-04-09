import sys
import time
from typing import Any


def measure_function(func, *args, **kwargs) -> tuple[float, float, Any]:
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()

    return end_time - start_time, sys.getsizeof(result), result
