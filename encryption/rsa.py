from encryption.fastmath import inversem, powm
from encryption.sieve import SieveEratosthenes
from array import array
import random


class RSAKey(object):
    PUBLIC_EXP = [17, 257, 65537]
    MIN_LEN = 8
    MAX_LEN = 16
    LEN_STEP = 4

    e: int
    d: int
    n: int

    def __init__(self, e: int, d: int, n: int):
        self.e = e
        self.d = d
        self.n = n

    @staticmethod
    def generate(length: int):
        if length == RSAKey.MAX_LEN:
            length -= 1
        minvalue = 1 << (length - 2)
        maxvalue = 1 << length
        sieve = SieveEratosthenes()
        sieve.fill(maxvalue)
        size = sieve.get_size()
        p = 0
        q = 0

        while p < minvalue:
            p = sieve.get(random.randrange(size))
        while q < minvalue:
            q = sieve.get(random.randrange(size))

        phi = (p - 1) * (q - 1)
        n = p * q
        e = 1

        for exp in RSAKey.PUBLIC_EXP:
            if exp < phi:
                e = exp

        d = inversem(e, phi)
        return RSAKey(e, d, n)

    @staticmethod
    def get_possible_len():
        possible = []
        for pl in range(RSAKey.MIN_LEN, RSAKey.MAX_LEN + 1, RSAKey.LEN_STEP):
            possible.append(str(pl))
        return possible


class RSAProcessor(object):
    key: RSAKey

    def __init__(self, key: RSAKey):
        self.key = key

    def encrypt(self, message: str):
        message = message.encode('utf-8')

        data = array('i', [len(message)])
        for b in message:
            data.append(powm(int(b), self.key.e, self.key.n))
        return data.tobytes()

    def decrypt(self, data):
        buffer = array('i')
        buffer.frombytes(data)
        out_buffer = bytearray()

        for num in buffer[1:]:
            out_buffer.append(powm(num, self.key.d, self.key.n))
        return out_buffer.decode('utf-8')
