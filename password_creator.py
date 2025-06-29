#!/usr/bin/env python3
import secrets
import random
from security import hash_password

def get_passwords():
    true_password = input("True password: ")
    n = int(input("Count of falas passwords: "))
    false_passwords = [input(f"Falase password #{i+1}: ") for i in range(n)]
    return true_password, false_passwords

def write_file(true_pw, false_pws): 
    salt = secrets.token_bytes(32)
    
    true_hash = hash_password(true_pw, salt, iterations=2)
    false_hashes = [hash_password(pw, salt, iterations=1) for pw in false_pws]
    
    all_hashes = [true_hash] + false_hashes
    random.shuffle(all_hashes)
    
    with open("passwords.txt", "w") as f:
        f.write(salt.hex() + "\n")
        for h in all_hashes:
            f.write(h + "\n")    

def main():
    true_pw, false_pws = get_passwords()
    write_file(true_pw, false_pws)
   
if __name__ == "__main__":
    main()
