from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# 1️⃣ Take input message
message = input("Enter your message: ").encode()

# 2️⃣ Generate AES key (16 bytes = 128-bit)
key = get_random_bytes(16)

# 3️⃣ Generate random IV (Initialization Vector)
iv = get_random_bytes(16)

# 4️⃣ Encrypt message
cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(pad(message, AES.block_size))

print("\n----- ENCRYPTION -----")
print("Original Message:", message.decode())
print("Encrypted (Ciphertext):", ciphertext)
print("AES Key:", key)
print("IV:", iv)

# 5️⃣ Decrypt the ciphertext
cipher_dec = AES.new(key, AES.MODE_CBC, iv)
decrypted = unpad(cipher_dec.decrypt(ciphertext), AES.block_size)

print("\n----- DECRYPTION -----")
print("Decrypted Message:", decrypted.decode())
