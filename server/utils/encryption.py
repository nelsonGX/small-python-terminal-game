import os
import base64
import hashlib

from ..proto import game
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

async def aes_encrypt(plaintext: bytes, key: bytes) -> bytes:
    iv = base64.b64decode(b'SdIDFUlELIE9VylveIc64w==')
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    pad_length = 16 - len(plaintext) % 16
    padded_plaintext = plaintext + bytes([pad_length] * pad_length)
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return ciphertext

async def aes_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    iv = base64.b64decode(b'SdIDFUlELIE9VylveIc64w==')
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    pad_length = padded_plaintext[-1]
    plaintext = padded_plaintext[:-pad_length]
    return plaintext

async def md5_protobuf_message(message) -> str:
    serialized_data = message.SerializeToString()
    md5_hash = hashlib.md5()
    md5_hash.update(serialized_data)
    return md5_hash.hexdigest()

async def encrypt(binary, message: game.Record):
    key = os.urandom(32)
    md5 = await md5_protobuf_message(message)
    await binary.write(key)
    await binary.write(md5.encode("utf-8"))
    proto = bytes(message.SerializeToString())
    proto = await aes_encrypt(proto, key)
    proto = await aes_encrypt(proto, md5.encode("utf-8"))  # Ensure md5 is bytes
    await binary.write(proto)

async def decrypt(binary) -> bytes:
    key = await binary.read(32)
    await binary.seek(32)
    md5 = await binary.read(32)
    await binary.seek(64)
    proto = await aes_decrypt(await binary.read(), md5)
    proto = await aes_decrypt(proto, key)
    return proto