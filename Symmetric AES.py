import hashlib
import math
import os

from Crypto.Cipher import AES

IV_SIZE = 16  # In real world its 128, it is initializattion vector
KEY_SIZE = 32  # it is the key, in real world it is 256
SALT_SIZE = 16  # More salt size , more difficult is hacking

clear_text = b'Hey how are you'

password = b'highly secured password'

salt = os.urandom(SALT_SIZE)  # added at the end to make hacking difficult

derived = hashlib.pbkdf2_hmac('sha256', password, salt, 100000,
                              dklen=IV_SIZE + KEY_SIZE)  # pbkdf2_hmac enables salt addition
# but sha256 does not
iv = derived[0:IV_SIZE]
key = derived[IV_SIZE:]  # fetching key and iv vector from derived

encrypted = salt + AES.new(key, AES.MODE_CFB, iv).encrypt(clear_text)
# We successfully created instance of the encryption
# This new function instantiates a new CFB cipher object
#print(encrypted)

#Now decryption

salt = encrypted[0:SALT_SIZE]
derived = hashlib.pbkdf2_hmac('sha256', password, salt, 100000, dklen=IV_SIZE+KEY_SIZE)
iv = derived[0:IV_SIZE]
key = derived[IV_SIZE:]

clear_text = AES.new(key, AES.MODE_CFB, iv).decrypt(encrypted[SALT_SIZE:])
print(clear_text)