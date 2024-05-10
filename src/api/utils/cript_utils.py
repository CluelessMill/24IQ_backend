from bcrypt import gensalt, hashpw
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from django.conf import settings

CYPHER_KEY = settings.CYPHER_KEY


def encrypt(data: str) -> bytes:
    cipher = Cipher(algorithms.AES(CYPHER_KEY), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_message = padder.update(data.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()
    return ciphertext


def decrypt(data: bytes) -> str:
    cipher = Cipher(algorithms.AES(CYPHER_KEY), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(data) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_message = unpadder.update(decrypted_message) + unpadder.finalize()
    return str(unpadded_message.decode())


def hash_password(password: str) -> bytes:
    salt = gensalt()
    hashed_password = hashpw(password.encode("utf-8"), salt)
    return hashed_password


def check_password(input_password: str, stored_password: bytes) -> bool:
    new_hash = hashpw(input_password.encode(encoding="utf-8"), stored_password)
    return new_hash == stored_password
