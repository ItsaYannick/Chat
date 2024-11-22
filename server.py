# Importera biblioteket socket och skapa en socket som kör IPv4 och TCP
import socket
import rsa
import threading

publicKey, privateKey = rsa.newkeys(512)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ställ in socketen att lyssna på enhetens alla adresser och specificera port
address = '192.168.142.100'
port = 12345
server_socket.bind((address, port))

# Lyssna på socket tills det kommer en anslutning
server_socket.listen(5)
print(f"Server is listening on {address}:{port}...")

clients = []

def broadcast(messege, senderSocket):
    for client, _ in clients:
        if client != senderSocket:
            try:
                client.send(messege)
            except Exception as e:
                print(f"Failed to send message to a client: {e}")
                client.close()
                remove_client(client)

def remove_client(client_socket):
    global clients
    clients = [client for client in clients if client[0] != client_socket]


def handleClient(client_socket, clientAddress):
    print(f"New connection from {clientAddress[0]}")

    client_socket.send(publicKey.save_pkcs1("PEM"))

    encClientName = client_socket.recv(1024)
    clientName = rsa.decrypt(encClientName, privateKey).decode("utf-8")
    

    try:
        
        
        print(f"Client {clientName} connected from {clientAddress[0]}.")

        broadcast(f"{clientName} has joined the chat.".encode('utf-8'), client_socket)
                    

        while True:
            # Receive an encrypted message
                    enc_message = client_socket.recv(1024)
                
                    if not enc_message:
                        break
                    try:
                        message = rsa.decrypt(enc_message, privateKey).decode('utf-8')
                        print(f"{clientName}: {message}")
                        # Broadcast the message to other clients
                        broadcast(f"{clientName}: {message}".encode('utf-8'), client_socket)
                    except Exception as e:
                        print(f"Error decrypting message from {clientName}: {e}")
                        break
    except Exception as e:
            print(f"Error handling client {clientAddress[0]}: {e}")
    finally:
        # Announce disconnection and remove the client
        print(f"{clientName} has disconnected.")
        broadcast(f"{clientName} has left the chat.".encode('utf-8'), client_socket)
        remove_client(client_socket)
        client_socket.close()
def acceptConnection():
     while True:
        client_socket, client_address = server_socket.accept()
        clients.append((client_socket, client_address))
        threading.Thread(target=handleClient, args=(client_socket, client_address), daemon=True).start()

if __name__ == "__main__":
    acceptConnection()

