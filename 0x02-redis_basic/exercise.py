#!/usr/bin/env python3
'''Redis data storage'''

import redis
import uuid
from typing import Union, Optional, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of times
    a method is called using Redis INCR."""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Generate the key using the qualified name of the
        method and increment the counter in Redis."""
        key = f"{method.__qualname__}:count"

        if isinstance(self._redis, redis.Redis):
            # Increment the counter in Redis
            self._redis.incr(key)

        # Call the original method and return its result
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    '''Defines a class Cache'''

    def __init__(self):
        '''Initialize the Cache with a Redis client and flush the database'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Defines a method that takes one argument
        data which can be of any type'''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable[[bytes],
            object]] = None) -> Optional[object]:
        """Retrieve data from Redis using the given key,
        optionally applying fn for conversion."""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """Convenience method to retrieve data as UTF-8 decoded string."""
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """Convenience method to retrieve data as integer."""
        return self.get(key, int)
