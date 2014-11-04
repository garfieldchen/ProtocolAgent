
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
    mgr = ProtocolAgent.Hub(2200, ("192.168.1.78", 2256), hooks_in, hooks_out, JsonAgent)
    mgr.start()
    mgr.serve_forever()
