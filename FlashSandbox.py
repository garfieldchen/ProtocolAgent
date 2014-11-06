
from gevent.server import StreamServer

import gevent
from gevent import Timeout

domain_content = '''<?xml version="1.0"?>
<cross-domain-policy>
    <allow-access-from domain="*" to-ports="*"/>
</cross-domain-policy>\0'''

def sandbox(port):
    def domain(sock, address):
        print "flash sandbox new connection: " + str(address)
        handle_sandbox(sock)
        with Timeout(2):
            sock.close()
        gevent.sleep(0)

    return StreamServer(('0.0.0.0', port), domain)


def handle_sandbox(sock):
        req = "<policy-file-request/>"
        data = sock.recv(len(req))
        assert (data == req)
        sock.send(domain_content)