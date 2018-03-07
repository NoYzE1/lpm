import random
import hashlib
import getpass
hexchars = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
def get_hexstring(length):
    hexstring = ""
    for i in range(length):
        hexstring += random.choice(hexchars)
    return hexstring
first_run = False
entries = {}
try:
    with open("lpm.db", mode='r') as f:
        lines = f.readlines()
        i = 0
        while i < len(lines)-1:
            l1 = lines[i].strip('\n')
            l2 = lines[i+1].strip('\n')
            l2 = l2.strip(' ')
            l2 = l2.split(',')
            l3 = []
            for c in l2:
                l3.append(int(c))
            entries[l1] = l3
            i += 2
except FileNotFoundError:
    with open("lpm.db", mode='w') as f:
        first_run = True
if first_run:
    p1 = 0
    p2 = 1
    while p1 != p2:
        p1 = hashlib.sha256(getpass.getpass().encode()).hexdigest()
        p2 = hashlib.sha256(getpass.getpass("Password again: ").encode()).hexdigest()
    p = p1
else:
    p = hashlib.sha256(getpass.getpass().encode()).hexdigest()
def save_entries():
    with open("lpm.db", mode='w') as f:
        for item in entries.items():
            f.write(item[0]+'\n')
            f.write(str(item[1]).lstrip('[').rstrip(']')+'\n')
def encrypt(entry):
    s = []
    i = 0
    for c in entry:
        s.append(ord(c) ^ ord(p[i]))
        i += 1
    return s
def decrypt(entry):
    s = ""
    i = 0
    for c in entry:
        s += chr(c ^ ord(p[i]))
        i += 1
    return s
def new_entry():
    b = input("Entry Name: ")
    ps = ""
    for i in range(32):
        ps += random.choice(hexchars)
    entries[b] = encrypt(ps)
    save_entries()
def create_entry():
    b = input("Entry Name: ")
    c = getpass.getpass()
    entries[b] = encrypt(c)
    save_entries()
def read_entry():
    print_entries()
    b = int(input("Entry: "))
    print()
    i = 1
    for entry in entries:
        if i == b:
            print(decrypt(entries[entry]))
            break
        else:
            i += 1
def delete_entry():
    pass
def print_entries():
    print()
    i = 1
    for entry in entries:
        print("{0}: {1}".format(i, entry))
        i += 1
    print()
while True:
    print()
    print("1: New Entry")
    print("2: Create Entry")
    print("3: Read Entry")
    print("4: Delete Entry")
    print("0: Exit\n")
    a = input()
    if a == "0":
        break
    elif a == "1":
        new_entry()
    elif a == "2":
        create_entry()
    elif a == "3":
        read_entry()
    elif a == "4":
        delete_entry()
