import os
from Crypto.Cipher import DES3

# Define as chaves a serem utilizadas
key1 = os.urandom(8)  # 64 bits
key2 = os.urandom(8)  # 64 bits
key3 = os.urandom(8)  # 64 bits

# Inicializa o cifrador TDES
cipher = DES3.new(key1 + key2 + key3, DES3.MODE_ECB)

# Cifra os dados
plaintext = b'Hello, world!'
ciphertext = cipher.encrypt(plaintext)

# Decifra os dados
decrypted = cipher.decrypt(ciphertext)

print("PlainText: ", plaintext)
print("Ciphertext: ", ciphertext)
print("Decrypted: ", decrypted)