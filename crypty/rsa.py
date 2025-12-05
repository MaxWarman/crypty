#!/usr/bin/python3

from __future__ import annotations

from secrets import randbelow
from typing import Tuple
from Crypto.Util.number import getPrime, isPrime, bytes_to_long, long_to_bytes

class RSA:
    def __init__(self, N: int, e: int = 65537, d: int|None = None):
        self.N = N
        self.e = e
        self.PK = (self.e, self.N)
        self.sk = None
        if d != None:
            self.d = d
            self.sk = (self.d, N)     
            w = randbelow(self.N)
            assert pow(pow(w, self.e, self.N), self.d, self.N) == w


    def encrypt(self, message: bytes) -> bytes:
        m = bytes_to_long(message)
        if m > self.N:
            raise ValueError(f"RSA.encrypt: Message too big (m > N)! m: {m.bit_length()}-bits, N: {self.N.bit_length()}-bits...")
        ciphertext = pow(m, self.e, self.N)
        return long_to_bytes(ciphertext)
    
    def decrypt(self, ciphertext: bytes) -> bytes:
        c = bytes_to_long(ciphertext)
        if c > self.N:
            raise ValueError(f"RSA.decrypt: Ciphertext too big (m > N)! m: {c.bit_length()}-bits, N: {self.N.bit_length()}-bits...")
        message = pow(c, self.d, self.N)
        return long_to_bytes(message)
    
    def export(self) -> Tuple[int, int, int]:
        return (self.N, self.e, self.d)
    
    @classmethod
    def new(cls, nbits: int = 2048, e: int = 65537) -> RSA:
        if nbits < 512:
            raise ValueError(f"RSA.__init__: Invalid nbits (required nbits >= 512): {nbits}")
        
        p = getPrime(nbits // 2)
        q = getPrime(nbits // 2)
        N = p * q
        phi = (p - 1) * (q - 1)
        d = pow(e, -1, phi)

        return RSA(N, e, d)
    
    @classmethod
    def import_from_sk(cls, sk: Tuple[int, int], primes: Tuple[int, int]) -> RSA:
        d = sk[0]
        N = sk[1]
        p = primes[0]
        q = primes[1]
        assert isPrime(p) and isPrime(q)
        assert N == p * q
        e = pow(d, -1, (p-1)*(q-1))

        return RSA(N, e, d)
    
    @classmethod
    def import_from_primes(cls, primes: Tuple[int, int], e: int = 65537):
        p = primes[0]
        q = primes[1]
        assert isPrime(p) and isPrime(q)
        N = p * q
        d = pow(e, -1, (p-1)*(q-1))
        
        return RSA(N, e, d)
        

def main():
    print("main")

    rsa = RSA.new(nbits=2048)

    m = b"Ale dobra kryptografia byc dla maupa"

    assert m == rsa.decrypt(rsa.encrypt(m))

if __name__ == "__main__":
    main()