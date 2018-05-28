#!/usr/bin/env python
# code: utf-8
from __future__ import print_function,division,absolute_import
from getlogger import getLogger; logger = getLogger(__name__)

import sys

from datetime import datetime
import random

import json
import redis

from websocket import create_connection
#getLogger("websocket")

from user_names import name_dict
from sentences import sentences_map

from config import cfg_redis,tts_channel,tts_ws

def ws_tts():
    redis_conn = redis.StrictRedis(**cfg_redis);
    pub = redis_conn.pubsub()
    pub.subscribe(tts_channel)

    ws_url = tts_ws #'ws://{:s}:{:d}/'.format('127.0.0.1',3000)

    def ws_send(msg_dict, ws=None):
        ws_ = ws if ws else create_connection(ws_url)
        ws_.send(json.dumps(msg_dict))
        result = ws_.recv()
        if not ws and ws_:
            ws_.close()

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
                    user_name = user_name.replace(' ','')
                    now = datetime.now()
                    hr  = now.hour
                    sen = random.choice(sentences_map[hr])
                    txt = user_name + ', ' + sen
                    logger.debug(('user_id=',user_id,'hr=',hr))
                    print('txt=',txt,file=sys.stderr)
                    ws_send(dict(tts=txt))
                except:
                    logger.error(('msg handling error',msg))


if __name__ == '__main__':
    ws_tts()

