
import ProtocolAgent
import FlashSandbox
from JsonAgent import JsonAgent

# retun
def hook_254(agent, cat, msg_id, body):
    print "------", agent, cat, msg_id, body

def hook_move(agent, cat, msg_id, body):
    return cat, msg_id + 1, body

def hook_buy(agent, cat, msg_id, body):
    body[1] += 1
    return cat, msg_id, body

hooks_in = {
    254: hook_254,
    94: hook_buy,
    7: hook_move
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
