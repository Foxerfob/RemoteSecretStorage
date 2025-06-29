#!/usr/bin/env python3
import os
import subprocess
import requests
import getpass
import hashlib
import base64
from cryptography.fernet import Fernet, InvalidToken

SERVER_URL = "http://localhost:5000"
END_POINT = "ENDPOINT"
CONTAINER_FILE = "secure_container.bin"
MAPPER_NAME = "secure_volume"

def main():
    print("=== Opening a secure container ===")
    
    if not os.path.exists(CONTAINER_FILE):
        print("[!] Error: container file not found!")
        return
    
    try:
        encryption_password = getpass.getpass("Enter password to decrypt the key: ")
        server_password = getpass.getpass("Enter server password: ")
        
        response = requests.get(
            f"{SERVER_URL}/{END_POINT}/get/{server_password}",
            timeout=5
        )
        
        if response.status_code != 200:
            print("\n[!] Access error. Code:", response.status_code)
            return
        
        encrypted_luks_password = response.text
        
        try:
            user_key = hashlib.sha256(encryption_password.encode()).digest()
            user_cipher = Fernet(base64.b64encode(user_key))
            luks_password = user_cipher.decrypt(encrypted_luks_password.encode()).decode()
            
        except InvalidToken:
            print("\n[!] Wrong password for key decryption!")
            return

        try:
            subprocess.run(
                ["cryptsetup", "open", CONTAINER_FILE, MAPPER_NAME],
                input=f"{luks_password}\n".encode(),
                check=True
            )
            print("\n[+] Container opened successfully!")
            print(f"Available as /dev/mapper/{MAPPER_NAME}") 
            
        except subprocess.CalledProcessError:
            print("\n[!] Error opening container.")
    
    except requests.exceptions.RequestException as e:
        print(f"\n[!] Server connection error: {str(e)}")

if __name__ == "__main__":
    main()
