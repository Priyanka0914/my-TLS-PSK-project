#clientpy1
import socket
from OpenSSL import SSL
from openssl_psk import patch_context
# from config import PSK_MAP #importing client id and psk


#dynamically choose client id and psk
# client_id = input("Enter client ID (client1, client2, client3): ").encode()



client_id = input("Enter client ID (client1, client2, client3): ").strip().encode()

if client_id == b"client1":
    CLIENT_ID = b"client1"
    CLIENT_PSK = bytes.fromhex("1a2b3c4d5e6f708192a3b4c5d6e7f809")
elif client_id == b"client2":
    CLIENT_ID = b"client2"
    CLIENT_PSK = bytes.fromhex("abcdefabcdefabcdefabcdefabcdefab")
elif client_id == b"client3":
    CLIENT_ID = b"client3"
    CLIENT_PSK = bytes.fromhex("1234567890abcdef1234567890abcdef")
else:
    # Use the entered client_id and a random PSK (likely to fail handshake)
    CLIENT_ID = client_id
    CLIENT_PSK = b"wrongpsk"

# ...rest of your code...
# if client_id not in PSK_MAP:
#     raise ValueError("Unknown client ID!")

# CLIENT_ID = client_id
# CLIENT_PSK = PSK_MAP[CLIENT_ID]
# CLIENT_ID = b"clientX"   # try invalid one
# CLIENT_PSK = b"wrongpsk"


patch_context()

def psk_client_callback(conn, identity_hint):

    print("[client] identity hint from server:", identity_hint)
    return (CLIENT_ID, CLIENT_PSK)

# creating a tls context
# context = SSL.Context(SSL.TLS_CLIENT_METHOD)
#create a TCP socket to connect

def run_client(host="127.0.0.1", port=4443):
    ctx = SSL.Context(SSL.TLSv1_2_METHOD)
    ctx.set_cipher_list(b'PSK-AES128-GCM-SHA256:PSK-AES128-CBC-SHA')
    ctx.set_psk_client_callback(psk_client_callback)

    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((host,port))

    ssl_sock=SSL.Connection(ctx,sock)
    ssl_sock.set_connect_state()

    # ssl_sock.do_handshake()
    # print("[client] handshake succeeded")

    try:
        ssl_sock.do_handshake()
        print("[client] handshake succeeded")

        msg = ssl_sock.recv(1024).decode()
        print("[client] server says:",msg)

        ssl_sock.send(b"ACK")
        


    # except SSL.Error as e:
    #     print("[client] Handshake failed - check PSK or ID:", e)
    #     ssl_sock.close()
    #     return
    

        while True:
            cmd = input("Enter command (TIME, DATE, EXIT) : ").strip()
            if not cmd:
                continue
            ssl_sock.send(cmd.encode())
            response=ssl_sock.recv(1024).decode()
            print("[client] server response:",response)

            if cmd.upper()=="EXIT":
                break

    except Exception as e:
        print("[client] TLS error:",e)
    finally:
        try:
            ssl_sock.shutdown()
        except Exception:
            pass
        ssl_sock.close()
        print("[client] connection closed")

if __name__ == "__main__":
    run_client()

    # response=conn.recv(1024).decode()
    # print("[client] response:",response)

     # if cmd.upper()=="EXIT":
    #    break
        # ssl_sock.send(b"Hello Server")
        # r=ssl_sock.recv(4096)
        # print("[client]received:",r)




    #     ssl_sock = SSL.Connection(context, sock)
    #     ssl_sock.set_connect_state()  # very important
    #     ssl_sock.connect(("127.0.0.1", 8443))
    #     ssl_sock.do_handshake()
    #     handshake_success = True
    #     print("TLS handshake complete (client)")
    # except SSL.Error as e:
    #     print("Handshake failed:", e)
    #     # ssl_sock.set_connect_state()
        # ssl_sock.connect(("127.0.0.1",8443))
        # ssl_sock = SSL.Connection(context, sock)
        # # ssl_sock.set_connect_state()
        # # ssl_sock.do_handshake()
        # print("TLS handshake complete(client)")

        # #sending message to server
        # ssl_sock.send(b"Hello Server,this is client!")

        # #receive the server response 
        # data=ssl_sock.recv(4096)
        # print("Received from the server:",data.decode())

    #     # print("Cipher suite:",ssl_sock.get_cipher_name())

    # except SSL.Error as e:
    #     print("Handshake failed:", e)
    # except OpenSSL.SSL.ZeroReturnError:
    #     print("Connection closed by server unexpectedly")    
    

    # finally:
    #     try:
    #         sock.shutdown()
    #     except Exception:
    #         pass
    #     sock.close()
    #     # ssl_sock.close()
    #     print("Connection closed(client)")

# if __name__=="__main__":
#     run_client()





# HOST = "127.0.0.1"
# PORT = 65432

# s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# s.connect((HOST,PORT))
# print("Handshake complete with server")       