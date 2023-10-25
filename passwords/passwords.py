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

'''def crackPhaseTwo():
    words = [line.strip().lower() for line in open('words.txt')]
    # words = [line.strip().lower() for line in open('testwords.txt')]

    passwords2 = open("passwords2.txt", "r")
    # passwords2 = open("testpasswords.txt", "r")
    solutions = open("cracked2.txt", "w")

    hashesComputed = 0
    for line in passwords2:
        user = getUser(line)
        passwordHash = getUnsaltedPasswordHash(line)
        # hashDict = {}

        while True:
            wordOne = words[random.randrange(0, len(words))]
            wordTwo = words[random.randrange(0, len(words))]
            curPassword = wordOne + wordTwo
            hashedGuess = hashPassword(curPassword)
            # store the password in dict to avoid repeats
            # hashDict[hashPassword(curPassword)] = curPassword
            
            hashesComputed += 1

            # print("user:", user)
            # print(f'Random password: {curPassword}\n')
            # print("rand password hash:", hashedGuess)
            # print("user hash:", passwordHash)
            # print(f'Random passwd hash: {hashPassword(curPassword)}\n')
            # print(f'Current user: {user}\n')
            # print(f'Current user passwd hash: {passwordHash}\n')
            # print(f'Dict len: {len(hashDict)}\n')
            # print("____________________")

            # found = hashDict.get(passwordHash)

            # if curPassword == "carcar":
            #     print("found the right passwd", curPassword)
            #     print("user's hash:", passwordHash, " computed hash:", hashPassword("carcar"))
            #     break

            # if found != None:
            if hashedGuess.strip() == passwordHash.strip():
                # password = hashDict[passwordHash]
                
                # solutions.write(f'{user}:{password}\n')
                # print(f'Found a password: {user}:{password}\n')
                solutions.write(f'{user}:{curPassword}\n')
                print(f'Found a password: {user}:{curPassword}\n')
                
                break

        # hashDict.clear()
        print("Number of hashes computeed: ", hashesComputed)
        
    passwords2.close()
    solutions.close()
'''

def crackPhaseTwo():
    words = [line.strip().lower() for line in open('words.txt')]
    # words = [line.strip().lower() for line in open('testwords.txt')]

    passwords2 = open("passwords2.txt", "r")
    # passwords2 = open("testpasswords.txt", "r")
    solutions = open("cracked2.txt", "w")

    hashesComputed = 0

    for line in passwords2:
        hashDict = {}

        user = getUser(line)
        passwordHash = getUnsaltedPasswordHash(line)

        startingWordIndex = 0

        # keep track of the starting word of the password
        # hash and store all possible passwords starting with that word
        # check to see if it matches user password
        # if yes, done. if no, move on to the next word
        while True:
            for word in words:
                curGuess = words[startingWordIndex] + word
                hashDict[hashPassword(curGuess)] = curGuess
                hashesComputed += 1
            
            found = hashDict.get(passwordHash)

            if found == None:
                hashDict.clear()
                startingWordIndex += 1
            else:
                hashDict.clear()
                print(f'Found a password: {user}:{curGuess}\n')
                solutions.write(f'{user}:{curGuess}\n')
                break

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