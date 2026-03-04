import bcrypt
import os
import time

class AuthManager:
    def __init__(self):
        self.master_file = "master.hash"
        self.lock_time = 30  # seconds
        self.failed_attempts = 0
        self.locked_until = None

    def create_master_password(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        with open(self.master_file, "wb") as f:
            f.write(hashed)

    def verify_master_password(self, password):
        if self.locked_until and time.time() < self.locked_until:
            print("Account locked. Try again later.")
            return False

        if not os.path.exists(self.master_file):
            return False

        with open(self.master_file, "rb") as f:
            stored_hash = f.read()

        if bcrypt.checkpw(password.encode(), stored_hash):
            self.failed_attempts = 0
            return True
        else:
            self.failed_attempts += 1
            if self.failed_attempts >= 3:
                self.locked_until = time.time() + self.lock_time
                print("Too many failed attempts. Locked for 30 seconds.")
            return False