# Ruben Boero

import binascii

# ----------- Diffie Hellman -----------

# find the x and y values for alice and bob
g = 7
p = 61

for i in range(p):
    if g**i % p == 30:
        print("x: ", i)

    if g**i % p == 17:
        print("y: ", i)


# ----------- RSA -----------

# https://en.wikipedia.org/wiki/RSA_(cryptosystem)

cipherText = [65426, 79042, 53889, 42039, 49636, 66493, 41225, 58964,
126715, 67136, 146654, 30668, 159166, 75253, 123703, 138090,
118085, 120912, 117757, 145306, 10450, 135932, 152073, 141695,
42039, 137851, 44057, 16497, 100682, 12397, 92727, 127363,
146760, 5303, 98195, 26070, 110936, 115638, 105827, 152109,
79912, 74036, 26139, 64501, 71977, 128923, 106333, 126715,
111017, 165562, 157545, 149327, 60143, 117253, 21997, 135322,
19408, 36348, 103851, 139973, 35671, 93761, 11423, 41336,
36348, 41336, 156366, 140818, 156366, 93166, 128570, 19681,
26139, 39292, 114290, 19681, 149668, 70117, 163780, 73933,
154421, 156366, 126548, 87726, 41418, 87726, 3486, 151413,
26421, 99611, 157545, 101582, 100345, 60758, 92790, 13012,
100704, 107995]

e = 17
n = 170171

# p = 449, q = 379
# n = 170171

# inefficiently computes the values of p and q (commented out bc its slow)
# for i in range(n):
#     for j in range(i):
#         if i * j == n:
#             print("The combo: " + str(i) + " and " + str(j) + " works.")

p = 449
q = 379

# d = 119537 (found in the for loop below)
for d in range(n):
    if (e * d) % ((p - 1) * (q - 1)) == 1:
        print("d: ", d)
        break

def decrypt(c, d, n):
    return (c**d % n)

# The decryption takes a minute, so I put it into a text file to save time on each subsequent 
# run of this program
f = open("cryptography/decryptMessage.txt", "x")

for c in cipherText:
    f.write(bin(decrypt(c, d, n)) + '\n')

f.close()

# https://blog.finxter.com/python-binary-string-to-ascii-string-and-vice-versa/
def bin_to_str(my_bin):
    my_int = my_int = int(my_bin, base=2)
    my_str = my_int.to_bytes((my_int.bit_length() + 7)//8, 'big').decode()
    return my_str

f = open("cryptography/decryptMessage.txt", "r")

for binary in f:
    binary = binary.strip()
    print(bin_to_str(binary), end="")
f.close()