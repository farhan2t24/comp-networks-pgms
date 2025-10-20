from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os

# Path where messages are stored
MESSAGE_FILE = "messages.txt"

# Function to encrypt a message
def encrypt_message(key, message):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return iv + ciphertext  # prepend IV to ciphertext

# Function to decrypt a message
def decrypt_message(key, ciphertext_iv):
    iv = ciphertext_iv[:16]
    ciphertext = ciphertext_iv[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

# ----------------- MAIN -----------------
def main():
    # Generate AES key for this session (in real app, teacher would have same key)
    # For demo, we hardcode a shared key
    key = b'ThisIsA16ByteKey'  # 16 bytes AES-128 key

    print("=== Secure Message Sender ===")
    message = input("Enter message to send to Teacher: ")

    # Encrypt the message
    encrypted = encrypt_message(key, message)

    # Save to file
    with open(MESSAGE_FILE, "ab") as f:
        f.write(encrypted + b"\n")

    print(f"Encrypted message saved to {MESSAGE_FILE}.\n")

    # Read back (simulate teacher receiving)
    print("Simulating teacher reading messages...\n")
    with open(MESSAGE_FILE, "rb") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            try:
                decrypted = decrypt_message(key, line.strip())
                print(f"Message {i+1} decrypted: {decrypted}")
            except:
                print(f"Message {i+1} could not be decrypted")

if __name__ == "__main__":
    main()
