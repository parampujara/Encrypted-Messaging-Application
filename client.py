import socket
from threading import Thread
import pyDH
from Crypto.Cipher import DES3

def rcv():
    while True:
        print(server.recv(1024).decode("utf-8"))

def pad(msg):
    while len(msg)%8 !=0:
        msg += ' '
    return msg 

def msg_peer(peer_port,msg):
    peer_ip = socket.gethostname()
    peer_info = (peer_ip,int(peer_port))
    server_peer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_peer.connect(peer_info)
    DH1 = pyDH.DiffieHellman()
    DH1_publickey = DH1.gen_public_key()
    server_peer.send(bytes(str(DH1_publickey),'utf-8'))
    F_publickey = server_peer.recv(1024).decode("utf-8")

    #key for symmetric key encryption
    DH1_secretkey = DH1.gen_shared_key(int(F_publickey))

    #Encrypting Message
    msg = pad(msg)
    cipher = DES3.new(str(DH1_secretkey)[0:24], DES3.MODE_ECB)
    encrypted_msg = cipher.encrypt(msg.encode("utf-8"))
    server_peer.send(encrypted_msg)
    server_peer.close()


def send(username):
    while True:
        msg_send = input()
        command,msg = msg_send.split(maxsplit=1)
        if(command == "create_group"):
            pass
        else:
            server.send(bytes(command,'utf-8'))
            details = server.recv(1024).decode("utf-8")
            #print(details)
            peername , portno = details.split(":")
            message = "-----------\n "+username+':"'+msg+'" \n-----------\n'
            msg_peer(portno,message)


def rcv_msg(client):
    print(client.recv(1024).decode("utf-8")) 

def chat(username,portno):
    SEND_THREAD = Thread(target=send,args=(username,))
    #RCV_THREAD = Thread(target=rcv)
    MSGS_THREAD = Thread(target=start_server,args=(portno,))
    SEND_THREAD.start()
    #RCV_THREAD.start()
    MSGS_THREAD.start()

def wait_for_connection(peer_server):
    while True:
        client, addr = peer_server.accept()
        DH2 = pyDH.DiffieHellman()
        DH2_publickey = DH2.gen_public_key()
        R_publickey = client.recv(1024).decode("utf-8")
        client.send(bytes(str(DH2_publickey),'utf-8'))

        #key for symmetric key decryption
        shared_key2 = DH2.gen_shared_key(int(R_publickey))
        encrypted_msg = client.recv(1024)

        #decrypting message
        cipher = DES3.new(str(shared_key2)[0:24], DES3.MODE_ECB)
        msg = cipher.decrypt(encrypted_msg)
        print(str(msg.decode("utf-8")))

def start_server(portno):
    PORT1 = int(portno)
    peer_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    peer_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    ADDR = (socket.gethostname(),PORT1)
    peer_server.bind(ADDR)
    peer_server.listen()
    ACCEPT_THREAD = Thread(target=wait_for_connection,args=(peer_server,))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
        #client1.send(bytes('Connection Established','utf-8'))
        #CLIENT_THREAD = Thread(target=rcv_msg,args=(peer_server,))
        #CLIENT_THREAD.start()
    

    

PORT = input('Enter port: ')
ADDR = (socket.gethostname(),int(PORT))

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.connect(ADDR)
print(server.recv(1024).decode("utf-8"))


#LOGIN or SIGNUP
print(server.recv(1024).decode("utf-8"))
sending = input()
server.send(bytes(sending,"utf-8"))

#SIGNUP
def login():
    if int(sending) == 1:
        print(server.recv(1024).decode("utf-8"))
        username = input()
        server.send(bytes(username,'utf-8'))
        print(server.recv(1024).decode("utf-8"))
        password = input()
        server.send(bytes(password,'utf-8'))
        print(server.recv(1024).decode("utf-8"))
        port_no = input()
        server.send(bytes(port_no,'utf-8'))
        server_response = server.recv(1024).decode("utf-8")
        print(server_response)
    elif int(sending) == 2:
        print(server.recv(1024).decode("utf-8"))
        username = input()
        server.send(bytes(username,'utf-8'))
        print(server.recv(1024).decode("utf-8"))
        password = input()
        server.send(bytes(password,'utf-8'))
        print(server.recv(1024).decode("utf-8"))
        port_no = input()
        server.send(bytes(port_no,'utf-8'))
        server_response = server.recv(1024).decode("utf-8")
        print(server_response)
    return server_response,username,port_no

server_response,username,portno = login()
if("Successful" in server_response):
    chat(username,portno)
    