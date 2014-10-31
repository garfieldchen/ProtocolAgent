
hooks_in = {
	
}

hooks_out = {
	
}

import ProtocolAgent
from JsonAgent import JsonAgent

hooks_in = {
	
}

hooks_out ={
	
}

if __name__ == "__main__":
	mgr = ProtocolAgent.Manager(2200, hooks_in, hooks_out, JsonAgent)
	mgr.serve_forever()
