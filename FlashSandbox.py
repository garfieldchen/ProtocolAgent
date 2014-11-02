
from gevent.server import StreamServer

domain_content = """
<?xml version="1.0">
<cross-domain-policy>
    <allow-access-from domain="*" to-ports="*"/>
</cross-domain-policy>"
"""


def sandbox(port):
    def domain(sock, addr):
        sock.send(domain_content)
        sock.flush()
        pass

    server = StreamServer(('0.0.0.0', port), domain)
    return server