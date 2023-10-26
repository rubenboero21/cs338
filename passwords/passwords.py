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
    encoded_password = password.encode('utf-8')
    hasher = hashlib.sha256(encoded_password)
    digest = hasher.digest()
    digest_as_hex = binascii.hexlify(digest)
    digest_as_hex_string = digest_as_hex.decode('utf-8')

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
    solutions = open("cracked2.txt", "w")
    extraInfo = open("hashCount.txt", "w")
    
    hashesToCrack = {}
    hashCount = 0
    
    # make a dict of hashed passwords and their corresponding usernames
    with open("passwords2.txt") as f:
        for line in f:
            user = getUser(line)
            hashedPassword = getUnsaltedPasswordHash(line)

            hashesToCrack[hashedPassword] = user

    # generate all the possible passwords, and check to see if it matches any of the hashes
    # saved in the dictionary
    for word1 in words:
        for word2 in words:
            password = word1 + word2
            hash = hashPassword(password)
            hashCount += 1

            found = hashesToCrack.get(hash)
            
            if found == None:
                continue
            else:
                solutions.write(f'{hashesToCrack[hash]}:{password}\n')
                extraInfo.write(f'Number of hashes computed: {hashCount}\n')

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