# author: garfieldchen

import struct

# length: 2 byge
class JsonAgent(ProtocolAgent.Agent):	
	#
	def send_msg(self, sock, msg_id, body):
		data = self.encode(msg_id, body)
		self.forward(sock, msg_id, data)

	# forward message 
	def forward(self, sock, msg_id, data):
		bin = struct.pack(">HHs", len(data) + 2, msg_id, data)
		sock.send(data)
		sock.flush()

	# message codec
	def decode(self, msg_id, data):
		return json.loads(data)

	def encode(self, msg_id, msg):
		return json.dumps(data)

	def read_pack(self, sock, fun):
		size = struct.unpack(">H", sock.read(2))
		data = sock.read(size)
		msg_id = struct.unpack_from(">H", data)
		body = data[2:]
		fun(msgId, data)