
import ProtocolAgent
import FlashSandbox
from JsonAgent import JsonAgent
import ProtocolId
import gevent
import time

import ChatAgent


my_ip = "192.168.1.78"

def hook_254(agent, cat, msg_id, body):
    print "------", agent, cat, msg_id, body

def hook_move(agent, cat, msg_id, body):
    return cat, msg_id + 1, body

def hook_buy(agent, cat, msg_id, body):
    body[1] += 1
    return cat, msg_id, body


def on_login(agent, cat, msg_id, body):
    print "--------------------------------- " + str(time.time())
    gevent.sleep(1.2)
    print "--------------------------------- " + str(time.time())
    gevent.sleep(3.2)
    print "--------------------------------- " + str(time.time())


def hook_auth(agent, cat, msg_id, body):
    if cat == ProtocolId.CAT_RESPONSE:
        ChatAgent.start_chat_agent(body, my_ip, chat_hook_in, chat_hook_out)

    return cat, msg_id, body

hooks_in = {
    254: hook_254,
    94: hook_buy,
    7: hook_move,

    ProtocolId.MSG_AVATAR_LOGIN: on_login
}

hooks_out = {
    ProtocolId.MSG_AUTH: hook_auth

}

########################################
def chat_x(agent, cat, msg_id, body):
    return cat, msg_id, body

chat_hook_in = {
    "default":chat_x

}

chat_hook_out = {
    "default":chat_x
}

#########################

if __name__ == "__main__":
    sandboxServer = FlashSandbox.sandbox(1843)
    sandboxServer.start()
    print "flash sandbox started"
    # sandboxServer.serve_forever()


    mgr = ProtocolAgent.Hub(2256, ("192.168.1.115", 2256), hooks_in, hooks_out, JsonAgent, 2, False)

    print "agent started at port: " + str(mgr.listen_port) + ", to remote " + str(mgr.addr_out)
    mgr.serve_forever()
