# Encoding:
Encoding converts data from one format to another so it can be safely transmitted or stored.It is not for security and does not require a secret key.
### Real‑world examples
* Encoding JWT payloads (Base64URL)
* Encoding images in HTML (data:image/png;base64)
* URL parameters in HTTP requests

# Encryption:
Transforms data into a secret format so that only authorized parties can read it. It is reversible, but only with the correct key.
### Real‑world examples
* HTTPS (TLS uses AES + RSA/ECC)
* Encrypting database columns (PII, PAN)
* Full disk encryption (BitLocker, FileVault)

# Hashing:
Converts data into a fixed‑length digest that cannot be reversed.
### Real‑world examples
* Password storage using bcrypt/Argon2
* Git commit integrity
* Checking file checksum (SHA‑256)

<img width="791" height="320" alt="image" src="https://github.com/user-attachments/assets/07746246-2d68-40d1-a5d9-fbbcf03f815e" />

🔐 Protect data from unauthorized access → Encryption
🔁 Transmit or store data safely across systems → Encoding
✅ Verify data or store passwords securely → Hashing
