from Crypto.Hash import SHA3_224
from Crypto.PublicKey import ECC

# Gerar um par de chaves pública e privada
private_key = ECC.generate(curve='P-224')
public_key = private_key.public_key()

# Assinar uma mensagem usando a chave privada
message = b"Hello, world!"
hash = SHA3_224.new(message).digest()
signature = private_key.sign(hash)

# Verificar a assinatura usando a chave pública
is_valid = public_key.verify(hash, signature)
if is_valid:
    print("A assinatura é válida")
else:
    print("A assinatura é inválida")