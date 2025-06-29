#!/usr/bin/env python3
import os
import subprocess
import requests
import getpass
import hashlib
import base64
from security import generate_strong_password
from cryptography.fernet import Fernet

SERVER_URL = "http://localhost:5000"
END_POINT = "ENDPOINT"
CONTAINER_FILE = "secure_container.bin"
CONTAINER_SIZE = "512" #MB

def create_luks_container():
    subprocess.run(["dd", "if=/dev/zero", f"of={CONTAINER_FILE}", "bs=1M", f"count={CONTAINER_SIZE}"], 
                  check=True)
    
    luks_password = generate_strong_password()
    subprocess.run(["cryptsetup", "luksFormat", CONTAINER_FILE], 
                  input=f"{luks_password}\n".encode(), 
                  check=True)
    
    return luks_password

def main():
    print("=== Creating a secure container ===") 
    luks_password = create_luks_container()
    
    encryption_password = getpass.getpass("Enter the key encryption password: ")
    server_password = getpass.getpass("Enter the server password (true for writing): ")

    user_key = hashlib.sha256(encryption_password.encode()).digest()
    key = Fernet.generate_key()
    cipher = Fernet(base64.b64encode(user_key))
    encrypted_luks_password = cipher.encrypt(luks_password.encode()).decode()

    response = requests.get(
        f"{SERVER_URL}/{END_POINT}/set/{server_password}/{encrypted_luks_password}",
        timeout=5
    )
    
    if response.status_code == 404:
        print("\n[+] Container created successfully!")
        print(f"[i] Size: {CONTAINER_SIZE}, file: {CONTAINER_FILE}")
        print("[!] If a fake server password is entered, the key will be destroyed!")
    else:
        print("\n[!] Error saving key. Code:", response.status_code)

if __name__ == "__main__":
    main()
