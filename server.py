#!/usr/bin/env python3
import hashlib
from flask import Flask
from security import check_password, delete_file

app = Flask(__name__)

END_POINT = "ENDPOINT"
SECRET_FILE ="secret.txt"
PASSWORD_FILE = "passwords.txt"
            
@app.route(f"/{END_POINT}/get/<password>")
def get_secret(password): 
    password_code = check_password(password, PASSWORD_FILE)

    if password_code == 1: 
        delete_file(SECRET_FILE)
        return "", 404 

    if password_code == 2:
        try:
            with open(SECRET_FILE, 'r') as f:
                return f.read(), 200
        except:
            return "", 404

    return "", 404 

@app.route(f"/{END_POINT}/set/<password>/<secret>")
def set_secret(password, secret): 
    password_code = check_password(password, PASSWORD_FILE)

    if password_code == 1:
        delete_file(SECRET_FILE)
        return "", 404 

    elif password_code == 2:
        try:
            with open(SECRET_FILE, 'w') as f:
                f.write(secret)
        except:
            pass

    return "", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
