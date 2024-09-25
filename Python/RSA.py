import rsa

(pubkey, privkey) = rsa.newkeys(512)

(bob_pub, bob_priv) = rsa.newkeys(512)

message = 'hello Bob!'.encode('utf8')

crypto = rsa.encrypt(message, bob_pub)

message = rsa.decrypt(crypto, bob_priv)

print(message.decode('utf8')) # >> hello Bob!

message2 = 'Go left at the blue tree'.encode()

signature = rsa.sign(message2, privkey, 'SHA-1')

message_after_transmision = 'Go left at the blue tree'.encode()

rsa.verify(message_after_transmision, signature, pubkey) # >> 'SHA-1'


"""
RSA can only encrypt messages that are smaller than the key.
A couple of bytes are lost on random padding, and the rest is available for the message itself.
For example, a 512-bit key can encode a 53-byte message
(512 bit = 64 bytes, 11 bytes are used for random padding and other stuff).
"""