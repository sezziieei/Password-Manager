import base64
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

class EncryptionManager:
    def __init__(self, master_password):
        self.salt_file = "salt.bin"
        self.key = self._derive_key(master_password)

    def _derive_key(self, password):
        if not os.path.exists(self.salt_file):
            salt = os.urandom(16)
            with open(self.salt_file, "wb") as f:
                f.write(salt)
        else:
            with open(self.salt_file, "rb") as f:
                salt = f.read()

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def encrypt(self, data):
        f = Fernet(self.key)
        return f.encrypt(data.encode()).decode()

    def decrypt(self, token):
        f = Fernet(self.key)
        return f.decrypt(token.encode()).decode()