Safe Habits.txt

Never click sketchy links - this can lead to man-in-the-middle attacks, seesion hijacking, browser hijacking, and xss.

Hover over links to see where they REALLY go, people can edit the text of links to make them more readable.

When reading an email check the Domain Name, if it is from @coinbase.rr.xyz.com do not trust it.

When entering a credit card enter it out of order. Keyloggers record in sequence.

For deciding what development methodology to use for a product(security vs availability):
![Desktop-vs-WebDev](https://github.com/user-attachments/assets/552e678d-f956-4786-a20a-422204511546)


UPDATED NOTE: with websockets you MUST create / replace the security of HTML

HTML is also stateless



### 🔐 Raw Sockets: Security Snapshot

Raw sockets give you **full control** over communication... which also means **full responsibility**.

#### 🔻 **Compared to HTTP/HTTPS:**
| **Aspect**                     | **HTTP/HTTPS (with Flask)**             | **Raw Sockets (custom server)**                 |
|-------------------------------|-----------------------------------------|-------------------------------------------------|
| **Encryption**                | Built-in via HTTPS (TLS)                | Must be implemented manually (e.g., OpenSSL)    |
| **Session Management**        | Built-in (cookies, headers, tokens)     | You must design session/token flow yourself     |
| **Authentication**            | Easy via headers + middleware           | Custom protocols needed                         |
| **Data Format Handling**      | JSON, form-data, etc. with parsing libs | Manual serialization/deserialization            |
| **Attack Surface**            | Standardized, hardened against injection| Higher risk if input isn't validated rigorously |

---

### 🧠 What You'd Need to Build for Raw Socket Security

If you go the raw socket route, you'd have to create:
- 🔑 **Session Token System**: A secure token that gets generated server-side, sent back to client, and validated with each connection.
- 🔄 **Handshake Protocol**: Something like `HELLO → CHALLENGE → RESPONSE` to confirm identity and establish trust.
- 🔒 **Encryption Layer**: Maybe TLS via OpenSSL or NaCl, unless traffic is going over a secure VPN.
- 🧹 **Input Sanitization**: Because raw sockets accept anything—must prevent buffer overflows, injection, malformed payloads.

---

### ✨ Bottom Line
- **Raw sockets can be secure**, but it’s like building your own seatbelt and airbag from scratch.
- **HTTP/HTTPS via Flask is simpler, battle-tested**, and has great scalability. And yes, you can still use Python `requests` or mobile apps to send POSTs—no HTML required.

Conclusion of Sockets vs Https:
Raw sockets feel low-level and “closer to the metal,” so it’s natural to assume they’d offer more control and thus more security. But as we’ve explored together, control doesn’t always equal safety. Sometimes it’s the guardrails—like HTTPS with Flask—that protect you from the things you didn’t even know you had to worry about.
Ask
=============================================================================================================================================================================================

🔑 Stages of a Token Lifecycle

1. Generation
The server creates a token (e.g. JWT or opaque string) when the user logs in or confirms a purchase.
Contains metadata like user ID, issue time, expiry, and permissions.

2. Delivery
Sent back to the client securely—often in the response to a POST request or via secure headers.
The client stores it temporarily (in memory, encrypted storage, etc.).

3. Usage
Attached to every request to authenticated endpoints (e.g. license validation, activation).
The server verifies it before allowing access or performing actions.

4. Expiration
Tokens have a time limit—usually minutes to hours—to reduce risk.
After expiry, the client must either:
Get a new token (via refresh flow), or
Re-authenticate fully

5. Revocation (Optional but powerful)
Server can invalidate specific tokens—e.g., if fraud is detected or license revoked.
Requires a blacklist or revocation list in memory or database.

🛡️ Why This Matters for You

For your license system:

You could issue a token at time of license generation, scoped to that user and device.
Use that token during activation to confirm identity + legitimacy.
Expire or revoke it when usage limits are reached or time runs out.
Helps prevent misuse or copied keys being activated on multiple machines.

✅ What You'll Get From That Setup

⏳ Lifetime and ExpirationTokens will self-expire based on timestamps you embed (like exp in JWT). No extra logic required during validation—just compare time.

🔐 Secure Storage and DeliveryThe token doesn’t need to be stored server-side unless you want full revocation. Clients keep it in memory or encrypted storage, and transmit it securely over HTTPS.

