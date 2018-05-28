#!/usr/bin/env python
# code: utf-8
from __future__ import print_function,division,absolute_import
from getlogger import getLogger; logger = getLogger(__name__)

import sys

from datetime import datetime
import random

import json
from websocket import create_connection
import redis

from user_names import name_dict
from sentences import sentences_map

#redis_conn = redis.StrictRedis(host='airi3.local',port=6379);
redis_conn = redis.StrictRedis(host='127.0.0.1',port=6379);
pub = redis_conn.pubsub()
pub.subscribe('tts2')

while True:
    msg = pub.get_message(timeout=120)
    if msg is None:
        logger.debug(('input wait timeout',))
        continue

    logger.debug(('msg=',msg))

    if msg['type'] == 'message':
        if 'data' in msg:
            user_id = msg['data']
            try:
                user_name = name_dict[user_id][0]
                now = datetime.now()
                hr  = now.hour
                sen = random.choice(sentences_map[hr])
                txt = user_name + ', ' + sen
                logger.debug(('user_id=',user_id,'hr=',hr))
                print('txt=',txt,file=sys.stderr)
            except:
                logger.error(('msg handling error',msg))


