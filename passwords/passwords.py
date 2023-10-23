# Ruben Boero

import hashlib
import binascii
import sys

# function taken from Jeff's sample code
def hashPasswd(password):
    encoded_password = password.encode('utf-8') # type=bytes
    hasher = hashlib.sha256(encoded_password)
    digest = hasher.digest() # type=bytes
    digest_as_hex = binascii.hexlify(digest) # weirdly, still type=bytes
    digest_as_hex_string = digest_as_hex.decode('utf-8') # type=string

    return digest_as_hex_string

def getUser(line):
    components = line.split(":")
    return components[0]

def getUnsaltedPasswordHash(line):
    components = line.split(":")
    return components[1]

# Create a dict of passwords and their hashed equivalents
words = open("words.txt", "r")

hashDict = {}

for word in words:
    word = str(word).lower()
    word = word.strip()
    hashDict[hashPasswd(word)] = word

words.close()

# Crack the passwords by comparing the hashes to our dictionary
passwords1 = open("passwords1.txt", "r")
solutions = open("cracked1.txt", "w")

for hash in passwords1:
    user = getUser(hash)
    passwordHash = getUnsaltedPasswordHash(hash)

    password = hashDict[passwordHash]

    solutions.write(f'{user}:{password}\n')
    # print(f'{user}:{password}')

passwords1.close()
solutions.close()