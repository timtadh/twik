#!/usr/bin/python

'''
Authentication methods for Twik. Based on crypt_framework <http://github.com/timtadh/crypt_framework>.
'''

from Crypto.Hash import SHA256

def normalize(text):
    s = ''
    for c in text:
        c = hex(ord(c))[2:]
        c = (2-len(c))*'0'+c
        s += c
    return s

def denormalize(text):
    s = ''
    buf = ''
    for c in text:
        buf += c
        if len(buf) == 2:
            s += chr(int(buf, 16))
            buf = ''
    return s

HASH_REPS = 50000

def __saltedhash(string, salt):
    sha256 = SHA256.new()
    sha256.update(string)
    sha256.update(denormalize(salt))
    for x in xrange(HASH_REPS): 
        sha256.update(sha256.digest())
        if x % 10: sha256.update(salt)
    return sha256

def saltedhash_bin(string, salt):
    return __saltedhash(string, salt).digest()

def saltedhash_hex(string, salt):
    return __saltedhash(string, salt).hexdigest()

def __hash(string):
    sha256 = SHA256.new()
    sha256.update(string)
    for x in xrange(HASH_REPS): sha256.update(sha256.digest())
    return sha256

def hash_bin(string):
    return __hash(string).digest()

def hash_hex(string):
    return __hash(string).hexdigest()
