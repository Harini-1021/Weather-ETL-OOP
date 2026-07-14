"""
Reusable decorators for the pipeline : @timer, @retry

"""

import functools
import time
from typing import Any, Callable
import requests

def timer(func: Callable) -> Callable:
    """Decorator that prints how long a function took to run."""
    @functools.wraps(func)
    def wrapper(*args:Any,**kwargs:Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start
        print(f"[timer] {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper 

def retry(max_attempts:int = 3, delay: float=1.0) -> Callable:
    """
    retries a function on requestException, up to max_attempts times,
    waiting 'delay' seconds between tries.
    """
    def decorator(func:Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Exception | None = None

            for attempt in range(1, max_attempts +1):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    last_exception = e
                    print(
                        f"[retry] {func.__name__} failed on attempt "
                        f"{attempt} / {max_attempts} : {e}"
                    )
                    if attempt < max_attempts:
                        time.sleep(delay)

            raise last_exception
        return wrapper
    return decorator
    
