from flask import Flask, request, jsonify, abort, render_template
import re
from cryptography.fernet import Fernet
"""Inspect HTTP header responses:  
Server:
Example: Server: nginx
This header shows what kind of server software is handling the request. It’s good for debugging, but it can also reveal server information (OS, version, etc)
that might be useful for attackers, so many people remove or obscure

1 Query String 
Example www,google.com/accounts?id=stevemunich123    Reveals a username.
The query string is the part of the URL that starts with a question mark (?). It’s often used for things like search terms or form inputs. 
Since users can modify these query strings, it’s important to handle them securely to prevent attacks like injections, where malicious code could be added.

2. Sanatize the OUTPUT from the server(not the input to it). If escaped characters make it back to the body it is a reflected XSS
Response Body
The HTTP response body is where the actual data lives—things like HTML, JSON, images, etc., that the server sends back to the client. 
To prevent injection attacks like Cross-Site Scripting (XSS), always sanitise and escape any data (especially user-generated content) before including it in the response.


=======================================Local Storage, Cookies, Cache================================================================
============================= =Important to prevent session hijacking & replay attacks ==============================================
3. Set - HttpOnly flag and the Secure flag to encrypt in transmission
Set-Cookie:
Example: Set-Cookie: sessionId=38af1337es7a8
This one sends cookies from the server to the client, which the client then stores and sends back with future requests. 
To keep things secure, make sure cookies are set with the HttpOnly flag (so they can’t be accessed by JavaScript) and the Secure flag (so they’re only sent over HTTPS).

4. Cache-Control: 
Example: Cache-Control: max-age=600
This header tells the client how long it can cache the response before checking with the server again. It can also prevent sensitive info from being cached if needed (using no-cache).

"""
# Generate a key (only once—store it securely!)
key = Fernet.generate_key()

# Save this somewhere safe and load it securely in production
fernet = Fernet(key)
def encrypt_field(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt_field(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()


app = Flask(__name__)

# Simple WAF filter to detect common injection patterns

#run the script then BASH:
# Hamerless request : curl -X POST http://127.0.0.1:5000/submit -d "name=Alice"
#dangerous request  : curl -X POST http://127.0.0.1:5000/submit -d "name=<script>alert('xss')</script>"

#2   submit data when you open the html file from File explor instead of being served from python
# Instead of " Data accepted! "

def waf_protect(f):
    def wrapped(*args, **kwargs):
        suspicious_patterns = [
            r"(?i)(union\s+select)",     # SQL injection
            r"(?i)(<script>)",           # XSS attack
            r"(?i)(drop\s+table)",       # SQL drop
            r"(?i)(--|\|\|)",            # SQL comments/logical ops
        ]
        payload = request.get_data(as_text=True) + str(request.args) + str(request.form)
        if any(re.search(pat, payload) for pat in suspicious_patterns):
            return jsonify({"error": "Blocked by WAF"}), 403
        return f(*args, **kwargs)
    return wrapped

@app.route('/submit', methods=['POST'])
@waf_protect
def submit():
    return jsonify({"message": "Data accepted!"})

@app.route('/', methods=['GET'])

def Homw():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
