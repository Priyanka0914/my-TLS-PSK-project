# TLS demo project  (python)

this is a simple client-server application that communicates securely using Transport Layer
Security (TLS) with Pre-Shared Key (PSK) authentication.

##  Setup

1. Clone or download this repository.  
2. Install Python 3.10+ (recommended).  
3. Install dependencies:
   ```bash
   pip install pyopenssl openssl-psk
   ```
4. Update `config.py` with your client identities and PSKs:
   ```python
   PSK_MAP = {
       b'client1': bytes.fromhex('1a2b3c4d5e6f708192a3b4c5d6e7f809'),
       b'client2': bytes.fromhex('abcdefabcdefabcdefabcdefabcdefab'),
       b'client3': bytes.fromhex('1234567890abcdef1234567890abcdef')
   }
   ```

---

## Running the Server

```bash
python server.py
```

The server will start listening on `127.0.0.1:4443`.

---

## Running the Client

```bash
python client.py
```

When prompted, enter a valid client ID (e.g., `client1`, `client2`, `client3`).  
Each client uses its own PSK from `config.py`.

---

## Example Run

### Server Output
```
[server] Listening on 127.0.0.1:4443...
[server] Connection from ('127.0.0.1', 51023)
[server] client identity: b'client1'
[server] handshake succeeded
[server] received command: TIME
```

### Client Output
```
Enter client ID (client1, client2, client3): client1
[client] handshake succeeded
Enter command (TIME,DATE,EXIT): time
[client] server response: 14:52:30
```

---

## Features
- ✅ Secure TLS with PSK (no certificates required)  
- ✅ Supports multiple clients with unique PSKs  
- ✅ Simple command interface (`TIME`, `DATE`, `EXIT`)  
- ✅ Error handling for wrong PSKs (handshake fails)  

---

## Stretch Goals
- Add more commands (e.g., `STATUS`, `HELLO`)  
- Extend config dynamically (load PSKs from file/db)  
- Document logs with screenshots
