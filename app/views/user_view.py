import asyncio
import datetime
import threading
import time

from app.views.base_view import BaseWebSocketHandler


class UserHandler(BaseWebSocketHandler):
    @classmethod
    def get_clients(cls):
        return cls.clients


def send_time():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    clients = UserHandler.get_clients()
    while True:
        for key in clients.keys():
            msg = str(datetime.datetime.now())
            clients[key]["object"].write_message(msg)
            print("write to client %s:%s" % (key, msg))
        time.sleep(10)


threading.Thread(target=send_time).start()
