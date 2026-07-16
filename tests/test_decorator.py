"""
Tests for the @timer and @retry decorators.
"""

import time

import pytest
import requests

from src.decorators import timer, retry


def test_timer_returns_original_result():
    """@timer should not alter the return value of the wrapped function."""
    @timer
    def add(a, b):
        return a + b

    assert add(2, 3) == 5


def test_timer_preserves_function_name():
    """@timer should preserve the original function's __name__ via functools.wraps."""
    @timer
    def my_function():
        pass

    assert my_function.__name__ == "my_function"


def test_retry_succeeds_on_first_try():
    """If the function never fails, @retry should call it exactly once."""
    call_count = {"count": 0}

    @retry(max_attempts=3, delay=0)
    def always_succeeds():
        call_count["count"] += 1
        return "success"

    result = always_succeeds()
    assert result == "success"
    assert call_count["count"] == 1


def test_retry_succeeds_after_failures():
    """If the function fails twice then succeeds, @retry should call it 3 times total."""
    call_count = {"count": 0}

    @retry(max_attempts=3, delay=0)
    def fails_twice_then_succeeds():
        call_count["count"] += 1
        if call_count["count"] < 3:
            raise requests.exceptions.RequestException("simulated failure")
        return "success"

    result = fails_twice_then_succeeds()
    assert result == "success"
    assert call_count["count"] == 3


def test_retry_gives_up_after_max_attempts():
    """If the function always fails, @retry should raise after max_attempts tries."""
    call_count = {"count": 0}

    @retry(max_attempts=3, delay=0)
    def always_fails():
        call_count["count"] += 1
        raise requests.exceptions.RequestException("always fails")

    with pytest.raises(requests.exceptions.RequestException):
        always_fails()

    assert call_count["count"] == 3


def test_retry_does_not_catch_unrelated_exceptions():
    """@retry should only catch RequestException, not other error types like ValueError."""
    call_count = {"count": 0}

    @retry(max_attempts=3, delay=0)
    def raises_value_error():
        call_count["count"] += 1
        raise ValueError("not a request error")

    with pytest.raises(ValueError):
        raises_value_error()

    # Should NOT have retried — ValueError isn't caught by @retry
    assert call_count["count"] == 1