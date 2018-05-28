#!/usr/bin/env python
# code: utf-8
from getlogger import getLogger; logger = getLogger(__name__)
import json
from websocket import create_connection
from config import tts_ws

"""
requirements:
  pip install websocket_client
"""

getLogger("websocket")


def create_ws_sender(args):
    """
    """

    ws_url = tts_ws # 'ws://{:s}:{:d}/'.format(args.host,args.port)

    def ws_send(msg_dict, ws=None):
        ws_ = ws if ws else create_connection(ws_url)
        ws_.send(json.dumps(msg_dict))
        result = ws_.recv()
        if not ws:
            ws_.close()

    return ws_send

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=3000)
    parser.add_argument('--host',type=str,default='127.0.0.1')
    parser.add_argument('messages',type=str,nargs='+')
    args = parser.parse_args()

    send = create_ws_sender(args)

    for message in args.messages:
        msg = json.loads(message)
        send(msg)
