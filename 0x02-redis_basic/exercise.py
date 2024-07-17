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
