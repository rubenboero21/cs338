# Ruben Boero

'''
This code is meant to be run from a command line (within the passwords folder).

There are 3 commands that can be run:

    python3 passwords 1
    python3 passwords 2
    python3 passwords 3

Each of these commands corresponds with password cracking for phase 1, 2, and 3 respectively.
'''

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

def crackPhaseOne():
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

    passwords1.close()
    solutions.close()

if __name__ == '__main__':

    if len (sys.argv) < 2:
        print('''Enter the phase that you would like to solve. \nFor example, 
                type:\n\npython3 passwords 1 \n\nto solve phase 1''')
        exit()
    
    if sys.argv[1] == "phase1" or sys.argv[1] == 1:
        crackPhaseOne()