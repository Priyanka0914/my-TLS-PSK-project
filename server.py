#serverpy

import socket
import datetime 
import threading
from OpenSSL import SSL
from openssl_psk import patch_context
from config import PSK_MAP

patch_context()

def psk_server_callback(conn,identity):
    conn.psk_identity = identity
    # print("[server] client identity:", identity)
    if identity in PSK_MAP:
        print(f"[server] accepted identity: {identity}")
        return PSK_MAP[identity]
    else:
        print(f"[server] Unknown PSK identity attempt: {identity}")
        return None

active_clients = {}


def handle_client(conn,addr,identity):
    try:                                     # to reject duplicate client ids 
        if identity in active_clients:
            print(f"[server] Duplicate login attempt: {identity} from {addr}")
            conn.send(b"ERROR: Identity already in use. Connection rejected.")
            conn.shutdown()
            conn.close()
            return
        else:
            active_clients[identity] = conn
            print(f"[server] {identity} connected from {addr}")
    
        conn.send(b"Handshake done.You are connected.")
        ack = conn.recv(1024)
        if ack == b"ACK":
            print(f"[server] client {identity} acknowledge connection")
        else:
            print(f"[server] client {identity} failed to acknowledge")

    # conn.do_handshake()   #you gotta correct this there is no variable ssl conn
    #     print(f"[server] Handshake succeeded with {addr}")
    # except SSL.Error as e:
    #     print(f"[server] Handshake failed for {addr} - possible wrong PSK: {e}")
    #     conn.close()
    #     return
  
        while True:
            data = conn.recv(1024)
            if not data:
                break

            command = data.decode().strip().upper()
            print(f"[server][{addr}] received command: {command}")
            print(f"[server] received command:{command}")

            if command == "TIME":
                response = datetime.datetime.now().strftime("%H:%M:%S")
            elif command == "DATE":
                response = datetime.datetime.now().strftime("%Y-%m-%d")
            elif command == "HELLO":
                response = f"Hello, {addr[0]}! How can I help you?"
            elif command == "STATUS":
                response = "Server is running fine"
            elif command == "EXIT":
                response = "Goodbye!"
                conn.send(response.encode())
                break
            else:
                response = "Unknown command"
            
            conn.send(response.encode())
    except Exception as e:
        print("[server] TLS error:",e)
        
    finally:
        if  identity in active_clients:
            del active_clients[identity]          # cleanup when client disconnects 
        try:
            conn.shutdown()           
        except Exception:
            pass                       #you might need to change both these lines
        conn.close()
        print(f"[server] connection closed:{addr}")

#creating tls context 
#setting up the TCP socket (creating tls server)

def run_server(host="127.0.0.1",port=4443):
    ctx = SSL.Context(SSL.TLSv1_2_METHOD)
    ctx.set_cipher_list(b'PSK-AES128-GCM-SHA256:PSK-AES128-CBC-SHA')
    ctx.use_psk_identity_hint(b"server-hint")
    # ctx.use_psk_identity_hint(b'demo-psk')
    ctx.set_psk_server_callback(psk_server_callback)

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1',4443))
    server_socket.listen(5)
    print(f"[server] Listening on {host}:{port}...")

    while True:
        try:  
            client_sock, addr = server_socket.accept()
            print(f"[server]Connection from {addr}")

            # client_sock.send(b"welcome")

            ssl_conn = SSL.Connection(ctx,client_sock)
            ssl_conn.set_accept_state()

            # Perform handshake here
            ssl_conn.do_handshake()
            print("[server] handshake succeeded")

            identity = getattr(ssl_conn, "psk_identity", b"unknown")
            threading.Thread(target=handle_client, args=(ssl_conn, addr, identity), daemon=True).start()

        except Exception as e:
            print("[server] error in accept/connection:",e)

if __name__ == "__main__":
    run_server()


# PSK_MAP = {
#     b"client1":b"secretPSK1",
#     b"client2":b"secretPSK2",
#     b"client3":b"secretPSK3",
#     b"clientX":b"secretPSKX",
# }
    #TLS conenction to client is made 
      
    #tls handshake 
    #     try:
    #         ssl_conn.do_handshake()
    #         print("TLS handshake successful !")
    #         print("Negotiated cipher suite:",ssl_conn.get_cipher_name())

    #     #exchanging data
    #         data = ssl_conn.recv(1024)
    #         print("Client says:",data.decode())
    #         ssl_conn.send(b"Hello Client")

    #     except Exception as e:
    #         print("Handshake failed:",e)

    # #closing connection
    #     finally:
    #         try:
    #             ssl_conn.shutdown()
    #         except Exception:
    #             pass
    #         ssl_conn.close()
        # ssl_conn.shutdown()
        # ssl_conn.close()





# HOST = "127.0.0.1"
# PORT = 65432

# s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# s.bind((HOST,PORT))
# s.listen()

# print(f"Server listening on {HOST}:{PORT}...")

# conn,addr = s.accept()
# print(f"Handshake complete,connected by {addr}")

# conn.close()
# s.close()
