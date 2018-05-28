#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function,division,absolute_import
import sys
import redis

r_ = redis.StrictRedis(host='127.0.0.1',port=6379) # (**cfg_redis)

def test_redis_pub(channel,message):
    r_.publish(channel,message)

def main():
    if len(sys.argv) < 2:
        print('Usage: test_ws_tts.py <user_id>',file=sys.stderr)
        sys.exit(1)
    test_redis_pub('tts2',sys.argv[1])

if __name__ == '__main__':
    main()
