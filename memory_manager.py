import json, os, base64
from typing import Optional
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

SALT_FILE = 'memory_salt.bin'

def _derive_key(password: str, salt: bytes) -> bytes:
    # Derive a 32-byte key for Fernet
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

class MemoryManager:
    def __init__(self, file_path="dream_memory.enc"):
        self.file_path = file_path
        # Ensure salt exists
        if not os.path.exists(SALT_FILE):
            with open(SALT_FILE, 'wb') as f:
                f.write(os.urandom(16))

    def _get_salt(self):
        with open(SALT_FILE, 'rb') as f:
            return f.read()

    def _ensure_empty_encrypted(self, fernet: Fernet):
        if not os.path.exists(self.file_path):
            # create an empty dict and write encrypted
            empty = fernet.encrypt(json.dumps({}).encode())
            with open(self.file_path, 'wb') as f:
                f.write(empty)

    def _load_decrypted(self, password: str):
        salt = self._get_salt()
        key = _derive_key(password, salt)
        fernet = Fernet(key)
        if not os.path.exists(self.file_path):
            self._ensure_empty_encrypted(fernet)
        with open(self.file_path, 'rb') as f:
            encrypted = f.read()
        try:
            decrypted = fernet.decrypt(encrypted)
        except Exception as e:
            raise ValueError("Incorrect password or corrupted memory file")
        return json.loads(decrypted.decode())

    def _save_encrypted(self, data: dict, password: str):
        salt = self._get_salt()
        key = _derive_key(password, salt)
        fernet = Fernet(key)
        encrypted = fernet.encrypt(json.dumps(data).encode())
        with open(self.file_path, 'wb') as f:
            f.write(encrypted)

    # Public API
    def save_dream(self, dream_text: str, timestamp: str, password: str) -> str:
        data = self._load_decrypted(password)
        dream_id = str(len(data) + 1)
        data[dream_id] = {"text": dream_text, "timestamp": timestamp}
        self._save_encrypted(data, password)
        return dream_id

    def save_result(self, dream_id: str, result: dict, password: str):
        data = self._load_decrypted(password)
        if dream_id in data:
            data[dream_id]["analysis"] = result
        self._save_encrypted(data, password)

    def load_all(self, password: str) -> dict:
        return self._load_decrypted(password)
