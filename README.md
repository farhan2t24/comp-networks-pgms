Encrypted messaging demo

This small demo shows a sender encrypting a message (AES-CBC via pycryptodome), storing ciphertext on the server, and a receiver viewing the decrypted message. The frontend also allows the receiver to optionally view the raw ciphertext after clicking.

Run (from project root with venv activated):

```powershell
& ".venv/Scripts/python.exe" -m pip install -r requirements.txt
& ".venv/Scripts/python.exe" server.py
```

Open http://127.0.0.1:5000/ in your browser.

Notes:
- This is a demo: the server stores keys in memory and returns the key when sending to the sender (so the sender can see the ciphertext and key). In a real system you would never send keys openly or persist them like this.
