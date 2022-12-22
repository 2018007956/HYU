'''
대칭키 암호화 - AES
hash 함수 - SHA256
비대칭키 암호화 - RSA
'''

import hashlib
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


BS = 16
pad = lambda s: s + (BS - len(s.encode('utf-8')) % BS) * chr(BS - len(s.encode('utf-8')) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

def aes(str):
    print('cipher type : AES')
    key = input('key(16/24/32):')
    key = key.encode('utf-8')
    iv = (chr(0)*16).encode('utf-8')
    encrypted = AES.new(key, AES.MODE_CBC,iv)
    str = pad(str)
    cipherText = encrypted.encrypt(str.encode('utf-8'))
    print('encrypted:',cipherText)

    encrypted = AES.new(key, AES.MODE_CBC,iv)
    plainText = encrypted.decrypt(cipherText)
    plainText = unpad(plainText)
    print('decrypted:',plainText)
    print()


def hash(str):
    print('hash type : SHA256')
    hash = hashlib.sha256(str.encode('utf-8'))
    print(hash.hexdigest())
    print()

def rsa(str):
    print('RSA')
    k_length = input('key length(x256, >=1024):')
    privateKey = RSA.generate(int(k_length))
    publicKey = privateKey.publickey()

    encrypted = PKCS1_OAEP.new(publicKey)
    cipherText = encrypted.encrypt(str.encode('utf-8'))
    print('encrypted:',cipherText)
    decrypted = PKCS1_OAEP.new(privateKey)
    plainText = decrypted.decrypt(cipherText)
    print('decrypted:',plainText)


str = input('original data:')
print()
aes(str)
hash(str)
rsa(str)

