# author: garfieldchen

import struct

import gevent
from gevent.server import StreamServer
import FlashSandbox

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
    def __init__(self, port, addr, hooks_in, hooks_out, clazz, len_size, with_sandbox = True):
        self.agent_class = clazz
        self.addr_out = addr
        self.hooks_in = hooks_in
        self.hooks_out = hooks_out
        self.with_sandbox = with_sandbox

        self.len_size = len_size

        self.agents = []
        self.listen_port = port

        self.server = StreamServer(('0.0.0.0', port), self.on_new_connection)

    def serve_forever(self):
        self.server.serve_forever()

    def on_new_connection(self, sock, address):
        try:
            print "new connection: " + str(sock) + " addr: " + str(address)
            agent = self.agent_class(sock, address, self.addr_out, self.hooks_in, self.hooks_out)

            gevent.spawn(self.net_loop, agent.sock_out, agent, agent.packet_out, "server :::")

            if self.with_sandbox:
                self.handle_sandbox(sock)

            self.net_loop(agent.sock_in, agent, agent.packet_in, "client :::")

            # gevent.sleep(0)
        except IOError as e:
            print "io error: " + str(e)
            agent.close()



    def net_loop(self, sock, agent, callback, name):
        while True:
            try:
                pack = sock.recv(self.len_size)
                if len(pack) == 0:
                    return

                pack_len = 0
                if self.len_size == 2:
                    pack_len, = struct.unpack(">H", pack)
                elif self.len_size == 4:
                    pack_len, = struct.unpack(">L", pack)

                data = ""
                if pack_len > 0:
                    data = sock.recv(pack_len)
                else:
                    return

                print name + "  data: " + data
                callback(data)
                gevent.sleep(0)
            except IOError:
                agent.close()
                raise


class Agent:
    def __init__(self, sock_in, addr_in, addr_out, hooks_in, hooks_out):
        self.sock_in = sock_in
        self.addr_in = addr_in

        self.addr_out = addr_out

        self.hooks_in = hooks_in
        self.hooks_out = hooks_out

        self.sock_out = gevent.socket.create_connection(addr_out)

    def packet_in(self, data):
        cat, msg_id, body = self.unpack(data)
        self.hook_message(self.sock_out, self.hooks_in, cat, msg_id, body)

    def packet_out(self, data):
        cat, msg_id, body = self.unpack(data)
        self.hook_message(self.sock_in, self.hooks_out, cat, msg_id, body)

    def hook_message(self, sock, hooks, cat, msg_id, data):
        handler = None
        if hooks:
            handler = hooks.get(msg_id) or hooks.get("default")

        if handler:
            ret = handler(self, cat, msg_id, self.decode(cat, msg_id, data))

            if ret:
                self.send_msg(sock, ret[0], ret[1], ret[2])
            else:
                self.forward(sock, cat, msg_id, data)
        else:
            self.forward(sock, cat, msg_id, data)

    def close(self):
        self.sock_in.close()
        self.sock_out.close()

    #
    def send_msg(self, sock, cat, msg_id, body):
        data = self.encode(cat, msg_id, body)
        self.forward(self, sock, cat, msg_id, data)

    # forward message
    def forward(self, sock, cat, msg_id, data):
        b = self.pack(cat, msg_id, data)
        print "to" + str(sock) + " " + str(sock.send(b))
        # sock.flush()

    # message codec
    def decode(self, cat, msg_id, data):
        pass

    def encode(self, cat, msg_id, msg):
        pass

    def unpack(self, data):
        pass

    def pack(self, cat, msg_id, data):
        pass


