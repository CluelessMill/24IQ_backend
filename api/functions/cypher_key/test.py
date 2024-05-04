import secrets
from binascii import unhexlify

binary_data = secrets.token_bytes(nbytes=16)  # KeyGen
print(binary_data)
hex_string = binary_data.hex()  # To store binary in .envv -> cast to hex
print(hex_string)
binary_data = unhexlify(hex_string)  # Hex from .env gets to binary
print(binary_data)
