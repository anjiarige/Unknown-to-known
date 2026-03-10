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

---

### The Setup [LFI Example]
A vulnerable PHP website has code like this: `<?php include($_GET['page']); ?>`
And the URL looks like: `http://target.com/index.php?page=home.php`
- Step 1 — Poison the log file
- Every time someone visits the website, Apache logs the request in /var/log/apache2/access.log, including the User-Agent header (which is the browser name). You can control this header. So you send a request with PHP code as your User-Agent:
`curl -A "<?php system($_GET['cmd']); ?>" http://target.com/`
Now the Apache log file contains a line like:
`10.10.14.8 - - [09/Mar/2026] "GET / HTTP/1.1" 200 ... "<?php system($_GET['cmd']); ?>"`
The PHP code is now sitting inside the log file. That's the **poisoning** part.
- Step 2 — Include the poisoned log
Now you use LFI to make the server include that log file:
`http://target.com/index.php?page=../../../var/log/apache2/access.log&cmd=whoami`
Here's what happens internally: PHP runs `include('/var/log/apache2/access.log')`. It reads through the log file, hits the line containing `<?php system($_GET['cmd']); ?>`, recognizes it as PHP code, and executes it. Since `cmd=whoami`, it runs whoami on the server and returns the output to you.
Why this is powerful
You now have remote code execution. You can change `cmd=whoam` to `cmd=id`, `cmd=cat /etc/shadow`, or even use it to spawn a reverse shell. All because the server executed a file it included, rather than just reading it.
That's the key — a normal path traversal would show you the raw log file text including the `<?php ... ?>` as plain text. But with LFI, the server treats it as code and runs it.

---
# What is SSRF?
`SSRF is when you trick the server into making HTTP requests on your behalf`. Instead of you directly accessing something, you make the server do it for you. This is dangerous because the server often has access to internal resources that you can't reach from the outside.

## Why is it dangerous?
Think of it like this. You're standing outside a building (the internet). There's a locked door (firewall). You can't get in. But there's an employee (the server) who can go inside freely. With SSRF, you trick that employee into going inside, grabbing information, and bringing it back to you.

Examples:
### Basic SSRF
A website has a feature that fetches a URL and shows you a preview. Like a "check if website is alive" tool:
http://target.com/fetch?url=http://google.com
The server-side code looks something like:
<?php echo file_get_contents($_GET['url']); ?>
The server takes your URL, fetches it, and returns the content. Works fine for normal use. But what if you change the URL to:
http://target.com/fetch?url=http://127.0.0.1:8080/admin
Now the server is making a request to itself on 127.0.0.1 (localhost). The admin panel might be blocked from the outside, but the server can access it because it's making the request locally. The response comes back to you, and you can now see the admin panel.

### SSRF to steal cloud credentials (very common and critical)
Cloud providers like AWS, GCP, and Azure run a metadata service on a special internal IP 169.254.169.254. This service contains sensitive information like access keys, tokens, and secrets. Only the server itself can access this IP.
http://target.com/fetch?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/
The server makes the request to the metadata service, grabs the AWS access keys, and returns them to you. Now you have:
- AWS Access Key ID
- Secret Access Key
- Session Token
- 
With these, you can log into their AWS account and access S3 buckets, databases, EC2 instances — basically their entire cloud infrastructure. This is how the `Capital One breach in 2019 ` happened. An attacker used SSRF to steal AWS credentials from the metadata service.

### Bypassing SSRF filters
Many apps try to block SSRF by checking if the URL contains 127.0.0.1 or localhost. But there are many bypasses:
Using decimal IP: http://target.com/fetch?url=http://2130706433:8080/admin (2130706433 is 127.0.0.1 in decimal)
Using IPv6: http://target.com/fetch?url=http://[::1]:8080/admin (::1 is localhost in IPv6)
Using a redirect: You host a page on your own server that redirects to 127.0.0.1. The app checks your external URL, says it's fine, but when the server follows the redirect, it ends up hitting localhost.
Using DNS rebinding: You set up a domain that first resolves to your external IP (passes the check), then resolves to 127.0.0.1 (when the server actually makes the request).

---

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

# SSRF
SSRF is an attack where you trick the server into making HTTP requests (or other protocol requests) on your behalf. Instead of you directly accessing an internal resource (which you can't), you make the server fetch it for you — because the server sits inside the trusted network.
`The core problem: the server trusts itself and its internal network, and the attacker abuses this trust by controlling what URLs the server fetches.`

`
Without SSRF:
Attacker → [Firewall] → BLOCKED → Internal Services

With SSRF:
Attacker → Vulnerable Server → Internal Services (no firewall between them)
`
## The Core Mechanism
- Normal Flow:
User → Sends URL to app: "https://example.com/image.png"
Server → Fetches the URL → Returns the content to user
(Everything is fine — it's a public URL)
POST /fetch-image
url=https://example.com/photo.jpg
→ Server downloads the image and displays it

- SSRF Attack Flow:
User → Sends URL to app: "http://169.254.169.254/latest/meta-data/"
Server → Fetches the URL → Returns cloud credentials to user
(Server accessed internal cloud metadata that the attacker can't reach directly)

User → Sends URL to app: "http://localhost:8080/admin"
Server → Fetches the URL → Returns admin panel contents
(Server accessed its own admin panel that's not exposed externally)
POST /fetch-image
url=http://localhost/admin
→ Server fetches its own admin panel and returns the content

The server made a request to **itself** — and since localhost requests bypass firewalls and authentication that's only enforced for external traffic, the attacker gets access to the admin panel.


# NMAP
Full port scan — `nmap -p- <target>`
Service/version detection — `nmap -sV <target>`
Enumerate ciphers & Check SSL certificate details: `nmap --script ssl-enum-ciphers,ssl-cert -p 443 <target>`
WAF detection script — `nmap --script http-waf-detect -p 80,443 <target>`


# Burp Suite BApp Store - Useful Extensions for Web Application Security Testing

## Must-Install (Always Use)

| # | Extension Name | Use Case | When to Use |
|---|---------------|----------|-------------|
| 1 | **ActiveScan++** | Extends Burp's active scanner with additional checks like host header injection, cache poisoning, and XML injection. | Every engagement — improves default scan coverage significantly. |
| 2 | **Autorize** | Replays requests with low-privilege session tokens to detect broken access control, IDOR, and privilege escalation. | Every engagement with authentication and role-based access. |
| 3 | **Logger++** | Advanced filterable logging of all Burp traffic. Search historical requests/responses with complex filters. | Every engagement — helps track and analyze all traffic efficiently. |
| 4 | **Param Miner** | Discovers hidden/unlinked parameters in requests. Finds web cache poisoning vectors, debug params, and secret API fields. | Every engagement — uncovers attack surface not visible in the UI. |
| 5 | **Collaborator Everywhere** | Injects Burp Collaborator payloads into headers (Referer, X-Forwarded-For, etc.) to find blind SSRF, OOB XXE, and blind injections. | Every engagement — catches blind vulnerabilities with no visible response. |
| 6 | **Turbo Intruder** | High-performance request sender using Python scripting. Sends thousands of requests/sec. | Race condition testing, brute-forcing tokens, credential stuffing at scale. |

## Install Based on Target

| # | Extension Name | Use Case | When to Use |
|---|---------------|----------|-------------|
| 7 | **JSON Web Tokens (JWT Editor)** | View, edit, and attack JWTs. Tests algorithm confusion (RS256→HS256), "none" algorithm bypass, and JWK injection. | When the target uses JWT-based authentication. |
| 8 | **InQL (GraphQL Scanner)** | Performs GraphQL introspection, maps schemas, and generates queries automatically. Finds hidden mutations and sensitive fields. | When the target uses GraphQL APIs. |
| 9 | **Upload Scanner** | Tests file upload features with polyglot files, content-type manipulation, and extension bypass techniques. | When the target has any file upload functionality. |
| 10 | **HTTP Request Smuggler** | Tests for HTTP request smuggling (CL.TE, TE.CL, TE.TE) vulnerabilities. | When a reverse proxy, CDN, or load balancer is in front of the app. |
| 11 | **CORS* (Additional CORS Checks)** | Tests for CORS misconfigurations by injecting various Origin headers. Catches wildcard, null origin, and reflected origin issues. | When the target has cross-origin API calls or uses CORS headers. |
| 12 | **WAF Detect / WAFNinja** | Identifies and fingerprints Web Application Firewalls to tailor bypass payloads. | When a WAF is suspected or confirmed in front of the target. |

## Nice to Have (Productivity Boosters)

| # | Extension Name | Use Case | When to Use |
|---|---------------|----------|-------------|
| 13 | **Hackvertor** | Tag-based encoding/decoding tool. Chain transformations (Base64, URL, Hex, Hash) directly inside requests. | When payloads need dynamic encoding/decoding before submission. |
| 14 | **Retire.js** | Flags known vulnerable JavaScript libraries (jQuery, Angular, etc.) and links to relevant CVEs. | Every engagement — passive check with zero effort. |
| 15 | **Reflected Parameters** | Highlights parameters whose values are reflected in responses. Saves time hunting for XSS. | XSS testing — pinpoints exactly where to focus. |
| 16 | **JS Link Finder** | Parses JavaScript files to extract hidden endpoints, API paths, and internal URLs. | Recon phase — discovers hidden attack surface in JS files. |
| 17 | **Content Type Converter** | Converts request bodies between JSON, XML, URL params, etc. Bypasses input validation or WAF rules. | When testing input handling across different content types. |
| 18 | **Error Message Checks** | Passively scans for verbose error messages, stack traces, DB errors, and debug info in responses. | Every engagement — passive detection of information disclosure. |
| 19 | **Software Vulnerability Scanner (Vulners)** | Analyzes server banners and fingerprints, cross-references against Vulners DB for known CVEs. | When identifying outdated server software (Apache, Nginx, PHP). |
| 20 | **IP Rotate** | Rotates source IP using cloud provider APIs to bypass rate-limiting or IP-based blocking. | When target has aggressive rate-limiting or IP-blocking mechanisms. |

---

## Quick Reference: Extension by Vulnerability Type

| Vulnerability Type | Recommended Extensions |
|--------------------|----------------------|
| **Broken Access Control / IDOR** | Autorize |
| **XSS (Cross-Site Scripting)** | Reflected Parameters, ActiveScan++ |
| **SSRF (Server-Side Request Forgery)** | Collaborator Everywhere |
| **SQL Injection / Blind Injection** | Collaborator Everywhere, ActiveScan++ |
| **JWT Attacks** | JWT Editor |
| **GraphQL Vulnerabilities** | InQL |
| **File Upload Bypass** | Upload Scanner |
| **HTTP Request Smuggling** | HTTP Request Smuggler |
| **CORS Misconfiguration** | CORS* |
| **Cache Poisoning** | Param Miner, ActiveScan++ |
| **Race Conditions** | Turbo Intruder |
| **Outdated Libraries / CVEs** | Retire.js, Vulners Scanner |
| **Hidden Endpoints / Recon** | JS Link Finder, Param Miner |
| **WAF Bypass** | WAF Detect, Content Type Converter |
| **Information Disclosure** | Error Message Checks |

---












`Think of it this way: XXE abuses a parser, SSRF abuses a fetcher, Path Traversal abuses a file reader, LFI abuses a file executor (locally), and RFI abuses a file executor (remotely).`
