
import ProtocolAgent
import FlashSandbox
from JsonAgent import JsonAgent

hooks_in = {

}

hooks_out = {

}

if __name__ == "__main__":
    sandboxServer = FlashSandbox.sandbox(843)
    sandboxServer.start()
    # sandboxServer.serve_forever()
    print "flash sandbox started"

    mgr = ProtocolAgent.Hub(2256, ("192.168.1.115", 2256), hooks_in, hooks_out, JsonAgent, 2, False)

    print "agent started at port: " + str(mgr.listen_port) + ", to remote " + str(mgr.addr_out)
    mgr.serve_forever()
