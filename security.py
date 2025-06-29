import os
import secrets
import hashlib

def hash_password(password: str, salt: bytes, iterations: int = 1) -> str:
    data = password.encode('utf-8')
    for _ in range(iterations):
        hasher = hashlib.sha256()
        hasher.update(data + salt)
        data = hasher.digest()
    return data.hex()

def check_password(password: str, file: str):
    try:
        with open(file, 'r') as f:
            lines = [line.strip() for line in f if line.strip()] 
        
        salt = bytes.fromhex(lines[0])
        stored_hashes = set(lines[1:])
        
        return  1 if hash_password(password, salt, 1) in stored_hashes else\
                2 if hash_password(password, salt, 2) in stored_hashes else\
                0
    except:
        return -1

def delete_file(file: str):
    if os.path.exists(file):
        with open(file, 'rb') as f:
            secret_len = len(f.read())
        with open(file, 'wb') as f:
            f.write(secrets.token_bytes(secret_len))
        os.remove(file) 

def generate_strong_password(length=32):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    return ''.join(secrets.choice(alphabet) for _ in range(length))
