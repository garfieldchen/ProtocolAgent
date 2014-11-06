# author: garfieldchen

import struct
import json
import ProtocolAgent


# length: 2 byte


class JsonAgent(ProtocolAgent.Agent):	
    # message codec
    def decode(self, cat, msg_id, data):
        return json.loads(data)

    def encode(self, cat, msg_id, msg):
        return json.dumps(msg)

    def unpack(self, data):
        pid, = struct.unpack_from(">H", data)
        cat = pid >> 12
        msg_id = pid & 0xFFF
        return cat, msg_id, data[2:]

    def pack(self, cat, msg_id, data):
        return struct.pack(">HH%ds"%len(data), len(data) + 2, (msg_id | cat << 12), data)
