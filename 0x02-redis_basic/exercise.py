#!/usr/bin/env python3
'''Redis data storage'''

import redis
import uuid
from typing import Union


class Cache:
    '''defines a class cache'''

    def __init__(self):
        '''Initialize the Cache with a Redis client and flush the database'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''defines a method that takes one
        argument data which can be of any type'''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable
            [[bytes], object]] = None) -> Optional[object]:
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
