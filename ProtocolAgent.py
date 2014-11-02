# author: garfieldchen

import gevent
from gevent.server import StreamServer

# 0. work flow
# client 						agent 						server
#             >>> message in 
#											<<< message out	 						

#
# 1. hook handler:
# def handler(agent, id, msg): None | (new_id, body) 
#
# 2.hooks map:
# {
# 	id: hook handler,
#   ...
# }


class Hub:
    def __init__(self, port, addr, hooks_in, hooks_out, clazz):
        self.agent_class = clazz
        self.addr_out = addr
        self.hooks_in = hooks_in
        self.hooks_out = hooks_out

        self.server = StreamServer(('0.0.0.0', port), self.on_new_connection)

    def serve_forever(self):
        self.server.serve_forever()

    def on_new_connection(self, sock, address):
        try:
            agent = self.agent_class(sock, address, self.addr_out, self, self.hooks_in, self.hooks_out)
            agent.update()
        except IOError:
            sock.close()


class Agent:
    def __init__(self, sock_in, addr_in, addr_out, hooks_in, hooks_out, hub):
        self.sock_in = sock_in
        self.addr_in = addr_in

        self.hook_in = hooks_in
        self.hook_out = hooks_out

        self.sock_out = gevent.socket.create_connection(addr_out)

        if not self.sock_out:
            raise IOError()
            pass

    def message_in(self, msg_id, data):
        self.hook_message(self.socke_out, self.hooks_in, msg_id, data)

    def message_out(self, msg_id, data):
        self.hook_message(self.socke_in, self.hooks_out, msg_id, data)

    def hook_message(self, sock, hooks, msg_id, data):
        handler = hooks or hooks[msg_id] or hooks["default"]
        if handler:
            new_id, body = handler(self, msg_id, self.decode(msg_id, data))

            if new_id:
                self.send_msg(sock, new_id, body)
            else:
                self.forward(sock, msg_id, data)
        else:
            self.forward(msg_id, data)

    def update(self):
        try:
            while True:
                self.read_pack(self.sock_in, self.message_in)
                self.read_pack(self.socke_out, self.message_out)
        except IOError:
            self.sock_in.close()
            self.sock_out.close()

    #
    def send_msg(self, sock, msg_id, body):
        pass

    # forward message
    def forward(self, sock, msg_id, data):
        pass

    # message codec
    def decode(self, msg_id, data):
        pass

    def encode(self, msg_id, msg):
        pass

    def read_pack(self, sock, fun):
        pass

