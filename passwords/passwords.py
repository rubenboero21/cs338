# Ruben Boero and Vanessa Heynes

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
import random

# function taken from Jeff's sample code
def hashPassword(password):
    encoded_password = password.encode('utf-8') # type=bytes
    hasher = hashlib.sha256(encoded_password)
    digest = hasher.digest() # type=bytes
    digest_as_hex = binascii.hexlify(digest) # weirdly, still type=bytes
    digest_as_hex_string = digest_as_hex.decode('utf-8') # type=string

    return digest_as_hex_string

def getUser(line):
    components = line.split(":")
    return components[0]

def getSaltedPasswordHash(line):
    components = line.split("$")
    components = components[3].split(":")
    return components[0]

def getSalt(line):
    components = line.split("$")
    return components[2]

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
        hashDict[hashPassword(word)] = word

    words.close()

    # Used to find the number of hashes computed for summary.txt
    # print(len(hashDict))

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

def crackPhaseTwo():
    words = [line.strip().lower() for line in open('words.txt')]

    passwords2 = open("passwords2.txt", "r")
    solutions = open("cracked2.txt", "w")
    
    hashDict = {}

    i = 0
    while i < 1: # there are 2734 possible passwords to crack

        # Generate a random password from 2 words, add it to a dict of possible 
        # passwords. Compare this password to the actual hashed passwords of each user.
        # If it's a match, add it to the output file, if not, try again with a new password.
        wordOne = words[random.randrange(0, len(words))]
        wordTwo = words[random.randrange(0, len(words))]

        curPassword = wordOne + wordTwo

        hashDict[hashPassword(curPassword)] = curPassword

        for hash in passwords2:
            user = getUser(hash)
            passwordHash = getUnsaltedPasswordHash(hash)

            found = hashDict.get(passwordHash, False)
            if found:
                password = hashDict[passwordHash]
                
                solutions.write(f'{user}:{password}\n')
                print(f'Found a password: {user}:{password}\n')

                i += 1

    passwords2.close()
    solutions.close()

def crackPhaseThree():
    words = [line.strip().lower() for line in open('words.txt')]
    passwords3 = open("passwords3.txt", "r")
    solutions = open("cracked3.txt", "w")

    for hash in passwords3:
        hashDict = {}

        user = getUser(hash)
        salt = getSalt(hash)
        passwordHash = getSaltedPasswordHash(hash)

        # compute all possible passwords for a single user
        for word in words:
            hashDict[hashPassword(salt + word)] = word

        # find the single password that the user actually has
        password = hashDict.get(passwordHash)

        solutions.write(f'{user}:{password}\n')

        hashDict.clear()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('''Enter the phase that you would like to solve. \nFor example, type:\n\npython3 passwords 1 \n\nto solve phase 1''')
        exit()

    elif len(sys.argv) == 2:
        if sys.argv[1] == "phase1" or sys.argv[1] == "1":
            crackPhaseOne()

        elif sys.argv[1] == "phase2" or sys.argv[1] == "2":
            crackPhaseTwo()

        elif sys.argv[1] == "phase3" or sys.argv[1] == "3":
            crackPhaseThree()