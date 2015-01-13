__author__ = 'garfield'

import ProtocolAgent
from JsonAgent import JsonAgent

def start_chat_agent(body, my_ip, hook_in, hook_out):
    ip = body["chat_host"]
    port = body["chat_port"]
    body["chat_host"] = my_ip
    mgr = ProtocolAgent.Hub(port, (ip, port), hook_in, hook_out, JsonAgent, 2, False)

    mgr.start()
