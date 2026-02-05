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

## Second‑order SQL injection:
Occurs when malicious input is stored in the database and later used unsafely in a SQL query, causing the injection to execute at a different point in the application.
`Malicious SQL input is stored safely at first, but executed later when the application retrieves and uses that stored data in a SQL query without proper sanitization.`
- NoSQL injection occurs when untrusted input is used to build NoSQL queries, allowing attackers to manipulate JSON‑based query logic.

<img width="645" height="288" alt="image" src="https://github.com/user-attachments/assets/08aedbca-fbbe-43dd-89f3-ec0f6c42f283" />

