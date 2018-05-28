#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function,division,absolute_import
import sys
import redis

from config import cfg_redis,tts_channel

r_ = redis.StrictRedis(**cfg_redis)

def test_redis_pub(channel,message):
    r_.publish(channel,message)

def main():
    if len(sys.argv) < 2:
        print('Usage: test_ws_tts.py <user_id>',file=sys.stderr)
        sys.exit(1)
    test_redis_pub(tts_channel,sys.argv[1])

if __name__ == '__main__':
    main()
