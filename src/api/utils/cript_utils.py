from bcrypt import gensalt, hashpw
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from django.conf import settings

CYPHER_KEY = settings.CYPHER_KEY


def encrypt(data: str) -> bytes:
    """
    Encrypts the provided data using AES encryption algorithm in ECB mode

    Parameters:
        data (str): The data to be encrypted

    Returns:
        bytes: The encrypted ciphertext

    Raises:
        None
    """

    cipher = Cipher(
        algorithm=algorithms.AES(key=CYPHER_KEY),
        mode=modes.ECB(),
        backend=default_backend(),
    )
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(block_size=128).padder()
    padded_message = padder.update(data=data.encode()) + padder.finalize()
    ciphertext = encryptor.update(data=padded_message) + encryptor.finalize()
    return ciphertext


def decrypt(data: bytes) -> str:
    """
    Decrypts the provided ciphertext using AES encryption algorithm in ECB mode

    Parameters:
        data (bytes): The ciphertext to be decrypted

    Returns:
        str: The decrypted plaintext

    Raises:
        None
    """

    cipher = Cipher(
        algorithm=algorithms.AES(key=CYPHER_KEY),
        mode=modes.ECB(),
        backend=default_backend(),
    )
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(data=data) + decryptor.finalize()
    unpadder = padding.PKCS7(block_size=128).unpadder()
    unpadded_message = unpadder.update(data=decrypted_message) + unpadder.finalize()
    return str(unpadded_message.decode())


def hash_password(password: str) -> bytes:
    """
    Hashes the provided password using bcrypt hashing algorithm

    Parameters:
        password (str): The password to be hashed

    Returns:
        bytes: The hashed password

    Raises:
        None
    """
    salt = gensalt()
    hashed_password = hashpw(password=password.encode(encoding="utf-8"), salt=salt)
    return hashed_password


def check_password(input_password: str, stored_password: bytes) -> bool:
    """
    Checks if the provided input password matches the stored hashed password

    Parameters:
        input_password (str): The password to be checked
        stored_password (bytes): The hashed password to be compared against

    Returns:
        bool: True if input password matches the stored hashed password, False otherwise

    Raises:
        None
    """

    new_hash = hashpw(
        password=input_password.encode(encoding="utf-8"), salt=stored_password
    )
    return new_hash == stored_password
