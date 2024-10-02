#*
# 
# this was largely made by gpt so it may not be secure so yeah :P
# 
# requires the cryptography libary
# pip install cryptography
# 
# needs open ssl 1.1
# you may need to run:
# sudo apt update
# sudo apt install libssl1.1
# to install it
# 
# on newer systems you may need to run
# sudo add-apt-repository ppa:deadsnakes/ppa
# sudo apt update
# sudo apt install libssl1.1
# 
# *#

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.kdf.kbkdf import KBKDFHMAC
from cryptography.hazmat.primitives.kdf.kbkdf import Mode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os # also os

# Key generation function
def generate_keypair():
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    return private_key, public_key

# Signing function
def sign_message(private_key, message):
    signature = private_key.sign(
        message,
        ec.ECDSA(hashes.SHA256())
    )
    return signature

# Signature verification function
def verify_signature(public_key, message, signature):
    try:
        public_key.verify(
            signature,
            message,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except:
        return False

# Encryption function (using public key)
def encrypt_message(private_key, peer_public_key, message):
    # Generate shared key from private key and peer's public key
    shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
    
    # Derive a symmetric key from the shared key
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    ).derive(shared_key)
    
    # Encrypt the message using the symmetric key
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(derived_key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message) + encryptor.finalize()
    
    return iv, ciphertext, encryptor.tag

# Decryption function (using private key)
def decrypt_message(private_key, peer_public_key, iv, ciphertext, tag):
    # Generate shared key from private key and peer's public key
    shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
    
    # Derive the same symmetric key
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    ).derive(shared_key)
    
    # Decrypt the message using the symmetric key
    cipher = Cipher(algorithms.AES(derived_key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    return plaintext

    shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
    
    # Derive the same symmetric key
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    ).derive(shared_key)
    
    # Decrypt the message using the symmetric key
    cipher = Cipher(algorithms.AES(derived_key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    return plaintext

# Helper function to serialize public key to bytes
def serialize_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

# Helper function to load public key from bytes
def load_public_key(public_key_bytes):
    return serialization.load_pem_public_key(public_key_bytes, backend=default_backend())

# Helper function to serialize private key to bytes
def serialize_private_key(private_key):
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

# Helper function to load private key from bytes
def load_private_key(private_key_bytes):
    return serialization.load_pem_private_key(private_key_bytes, password=None, backend=default_backend())

# Export private key to text (PEM format)
def export_private_key_to_text(private_key):
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()  # No password
    )
    return private_key_pem.decode('utf-8')  # Convert bytes to string

# Export public key to text (PEM format)
def export_public_key_to_text(public_key):
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return public_key_pem.decode('utf-8')  # Convert bytes to string


# Load private key from text (PEM format)
def load_private_key_from_text(private_key_pem_text):
    private_key = serialization.load_pem_private_key(
        private_key_pem_text.encode('utf-8'),  # Convert string to bytes
        password=None,  # If the key was encrypted, you'd pass the password here
        backend=default_backend()
    )
    return private_key

# Load public key from text (PEM format)
def load_public_key_from_text(public_key_pem_text):
    public_key = serialization.load_pem_public_key(
        public_key_pem_text.encode('utf-8'),  # Convert string to bytes
        backend=default_backend()
    )
    return public_key


# Example usage
if __name__ == "__main__":

    # Key generation
    private_key, public_key = generate_keypair()
    peer_private_key, peer_public_key = generate_keypair()  # Peer's key pair

    #key exportation
    private_key_text = export_private_key_to_text(private_key)
    public_key_text = export_public_key_to_text(public_key)
    print("private:",private_key_text, private_key.key_size)
    print("public:",public_key_text, public_key.key_size)

    # Message to be signed, encrypted
    message = b"This is a secret message."
    # Signing and verif ying
    signature = sign_message(private_key, message)
    assert verify_signature(public_key, message, signature), "Signature verification failed!"
    print("signature:",signature)

    # Encryption and decryption using private key and peer's public key
    iv, ciphertext, tag = encrypt_message(private_key, peer_public_key, message)
    encrypted_message = {"iv":iv, "ciphertext":ciphertext, "tag":tag }
    decrypted_message = decrypt_message(peer_private_key, public_key, iv, ciphertext, tag)
    
    print(encrypted_message)
    assert message == decrypted_message, "Decryption failed!"
    print("ECC encryption and decryption were successful.")
