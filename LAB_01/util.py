import sys
from hashlib import md5


def load_data_and_generate_simhash():
    N = int(next(sys.stdin).strip())
    simhashes = [generate_sim_hash(next(sys.stdin).strip()) for _ in range(N)]
    Q = int(next(sys.stdin).strip())
    queries = [list(next(sys.stdin).strip().split()) for _ in range(Q)]
    return simhashes, queries


def bin_list_to_hex(bin_list: list) -> str:
    return hex(int("".join(bin_list), 2))[2:].zfill(32)


def bin_hash(text: str) -> str:
    _hash = md5(text.encode()).hexdigest()
    return bin(int(_hash, 16))[2:].zfill(128)


def generate_sim_hash(text: str) -> str:
    simhash = [0] * 128
    units = text.split()

    for unit in units:
        _hash = bin_hash(unit)

        for i, bit in enumerate(_hash):
            if bit == "1":
                simhash[i] += 1
            else:
                simhash[i] -= 1

    simhash = ["1" if i >= 0 else "0" for i in simhash]
    return bin_list_to_hex(simhash)


def hamming_distance_within(simhash1: str, simhash2: str, max_distance: int) -> int:
    xor = int(simhash1, 16) ^ int(simhash2, 16)
    return bin(xor).count("1") <= max_distance
