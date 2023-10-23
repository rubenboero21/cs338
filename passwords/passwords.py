# Ruben Boero

import hashlib
import binascii

# function taken from Jeff's sample code
def hashPasswd(password):
    encoded_password = password.encode('utf-8') # type=bytes
    hasher = hashlib.sha256(encoded_password)
    digest = hasher.digest() # type=bytes
    digest_as_hex = binascii.hexlify(digest) # weirdly, still type=bytes
    digest_as_hex_string = digest_as_hex.decode('utf-8') # type=string

    return digest_as_hex_string


words = open("/Users/rubenboero/Desktop/cs338/passwords/words.txt", "r")

hashDict = {}

for word in words:
    word = word.strip()
    word = str(word).lower()
    print(word)

    hashDict[word] = hashPasswd(word)

print(hashDict["marmot"])

words.close()