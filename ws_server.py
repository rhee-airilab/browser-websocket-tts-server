#!/usr/bin/env python
# code: utf-8
from getlogger import getLogger; logger = getLogger(__name__)
import json
from websocket_server import WebsocketServer

"""
requirements:
  pip install websocket_server
"""

def start_ws_server(args):
    """
    """

    server = WebsocketServer(args.port, host=args.host)

    def send(msg,client):
        try:
            message = json.dumps(msg)
            server.send_message(client,message)
        except:
            logger.exception(('ws send error'))

    def broadcast(msg):
        try:
            server.send_message_to_all(msg)
        except:
            #logger.exception(('ws send error'))
            pass

    def new_client(client, server):
        logger.info(('connected',client['id']))
        message = json.dumps({'message':'connected','client':client['id']})
        broadcast(message)

    def client_left(client, server):
        logger.info(('disconnected',client['id']))
        message = json.dumps({'message':'disconnected','client':client['id']})
        broadcast(message)

    def message_received(client, server, message):
        logger.info(('message_received',len(message),message[:100]))

        try:
            msg = json.loads(message)
            new_message = json.dumps({'message':'message','client':client['id'],'content':msg})
            broadcast(new_message)
        except:
            logger.exception(('ws message handler error'))
            resp_message = json.dumps({'message':'error','description':'server error'})
            send(resp_message,client)
            return

        resp_message = json.dumps({'message':'result','description':'ok'})
        send(resp_message,client)

    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=3000)
    parser.add_argument('--host',type=str,default='127.0.0.1')
    args = parser.parse_args()
    start_ws_server(args)
