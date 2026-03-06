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

## XXE (XML External Entity)
Example for DTD with External Entity

* XXE is a vulnerability that occurs when an application parses attacker‑controlled XML and allows external entities to be resolved.
- XXE occurs when untrusted XML is parsed by a misconfigured XML parser that allows external entity resolution, enabling attackers to read files, perform SSRF, or cause DoS. The critical factor is whether DTD and external entities are enabled.

```
<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE data [
    <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>

<data>
    &xxe;
</data>
```

**Everything inside the DOCTYPE brackets is the DTD**

```
<!DOCTYPE data [
    <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
```

❗ **NO <!DOCTYPE> → NO DTD → NO XXE**

# Path Traversal:
(aka Directory Traversal) is a vulnerability where an attacker can read arbitrary files from the filesystem by manipulating file paths.
- Accepts a filename or path
- Uses it in functions like:
* open()
* readFile()
* file_get_contents()
**Does NOT execute the file**

`
GET /download?file=../../../../etc/passwd
`
# LFI:
It happens when an attacker can include a local file into application execution.
This usually happens with:
- include
- require
- include_once
- require_once

>[!Important]
> **Path Traversal allows attackers to read arbitrary files, while LFI allows attackers to include and potentially execute local files; LFI is more dangerous because it runs files in an execution context and can reach RCE using wrappers.**

```
Vulnerable Code

include($_GET['page'] . ".php");
```

<img width="645" height="283" alt="image" src="https://github.com/user-attachments/assets/78ec0843-89c0-466f-9d98-af191e502fca" />

>[!Note]
>✅ LFI often uses Path Traversal
>
>❌ Path Traversal does not require LFI

<img width="660" height="435" alt="image" src="https://github.com/user-attachments/assets/dad6eb4b-1bb4-4ceb-821c-e3048cebf19d" />

Usage:
?page=php://filter/convert.base64-encode/resource=index.php

📌 Wrappers are primarily dangerous in PHP

## Insecure deserialization:
### What Is Serialization / Deserialization?
- `Serialization` is the process of converting an object in memory (like a Java object, Python dict, or PHP class instance) into a format that can be stored or transmitted — such as a byte stream, JSON, XML, or a language-specific format.
- `Deserialization` is the reverse: taking that serialized data and reconstructing it back into a live object in memory.

The vulnerability arises when an application deserializes untrusted data without validation. An attacker can craft a malicious serialized object that, when deserialized, triggers unintended actions like remote code execution, privilege escalation, or data tampering.

### Why Is It Dangerous?
When an application deserializes data, it doesn't just restore values — it can reconstruct entire objects, invoke constructors, and trigger special methods `(like __wakeup() in PHP`, `readObject() in Java`, or `__reduce__() in Python)`. Attackers exploit these "**magic methods**" to chain together existing classes in the application (called gadget chains) to achieve code execution.

### How to Prevent It
- Never deserialize untrusted data — this is the golden rule
- Use safe data formats like JSON instead of language-native serialization (JSON doesn't carry code, only data)
- Integrity checks — sign serialized objects with HMAC so tampering is detected
- Allowlist classes — if you must deserialize, restrict which classes can be instantiated (Java's ObjectInputFilter, for example)
- Isolate deserialization — run it in a low-privilege, sandboxed environment
- Monitor — log deserialization failures and watch for common exploit signatures


`Think of it this way: XXE abuses a parser, SSRF abuses a fetcher, Path Traversal abuses a file reader, LFI abuses a file executor (locally), and RFI abuses a file executor (remotely).`
