# Faster than google
map = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
hex_to_bytes = {h: bin(i)[2:].zfill(4) for i, h in enumerate(map)}

def make_bytes(hex_data):
    return ''.join(hex_to_bytes[h] for h in hex_data)

with open('input') as handle:
    raw = [line.strip() for line in handle.readlines()]
    packets = [make_bytes(line) for line in raw]

def trim(packet):
    return '' if set(packet) == {'0'} else packet

versions = [int(packet[:3], 2) for packet in packets]
def parse(packet):
    version, packet = int(packet[:3], 2), packet[3:]
    type_id, packet = int(packet[:3], 2), packet[3:]
    if type_id == 4:
        literal = []
        while True:
            assert packet
            chunk, packet = packet[:5], packet[5:]
            literal.append(chunk[1:])
            if chunk[0] == '0': break
        literal = ''.join(literal)
        return version, type_id, int(literal, 2), trim(packet)
    else:
        length_id, packet = int(packet[:1], 2), packet[1:]
        if length_id == 0:
            length, packet = int(packet[:15], 2), packet[15:]
            to_parse, packet = packet[:length], packet[length:]
            subpackets = []
            while to_parse:
                *subpacket, to_parse = parse(to_parse)
                subpackets.append(subpacket)
            return version, type_id, subpackets, trim(packet)
        else:
            n_subpackets, packet = int(packet[:11], 2), packet[11:]
            subpackets = []
            for _ in range(n_subpackets):
                *subpacket, packet = parse(packet)
                subpackets.append(subpacket)
            return version, type_id, subpackets, trim(packet)

from functools import reduce
import operator as op

def evaluate(version, type_id, payload):
    if type_id == 4:
        return payload
    elif type_id == 0:
        return sum(evaluate(*subpacket) for subpacket in payload)
    elif type_id == 1:
        return reduce(op.mul, [evaluate(*subpacket) for subpacket in payload])
    elif type_id == 2:
        return min(evaluate(*subpacket) for subpacket in payload)
    elif type_id == 3:
        return max(evaluate(*subpacket) for subpacket in payload)
    elif type_id == 5:
        assert len(payload) == 2
        first, second = [evaluate(*subpacket) for subpacket in payload]
        return 1 if first > second else 0
    elif type_id == 6:
        assert len(payload) == 2
        first, second = [evaluate(*subpacket) for subpacket in payload]
        return 1 if first < second else 0
    elif type_id == 7:
        assert len(payload) == 2
        first, second = [evaluate(*subpacket) for subpacket in payload]
        return 1 if first == second else 0


def sum_versions(packet_tree):
    version, _, subpackets = packet_tree
    if isinstance(subpackets, list):
        return version + sum(sum_versions(s) for s in subpackets)
    else:
        return version

*parsed, _ = parse(packets[0])
print(sum_versions(parsed))


*parsed, _ = parse(packets[0])
print(evaluate(*parsed))
