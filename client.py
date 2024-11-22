# Importera biblioteket socket och skapa en socket som kör IPv4 och TCP
import socket
import time
import threading
import rsa


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Lägg in adress och port och anslut till servern
address = '192.168.142.100'
port = input('Skriv in serverns port: ')

socket.connect((address, int(port)))
print("Connected to: "+ address)

publicKey_PEM = socket.recv(1024)
publicKey = rsa.PublicKey.load_pkcs1(publicKey_PEM)
print("publicKey recieved")

name = input("Enter Name: ")
encName = rsa.encrypt(name.encode('utf-8'), publicKey)
socket.send(encName)

def listen(socket):
    while True:
        messege = socket.recv(1024).decode('utf-8')
        print(messege)


thread1 = threading.Thread(target=listen, args=(socket,))
thread1.daemon = True
thread1.start()

while True:


    # Efterfråga användarens namn som sedan skickas till servern i formatet UTF-8
    text = input("> ")
    if text =="EXIT":


        print("Disconnecting")
        time.sleep(1)
        print("Disconnecting.")
        time.sleep(1)
        print("Disconnecting..")
        time.sleep(1)
        print("Disconnecting...")
        time.sleep(1)
        socket.close()
        break

    
    encMessage = rsa.encrypt(text.encode('utf-8'), publicKey)

    socket.send(encMessage)

    # Samla in svaret från servern och skriv ut i terminalen
    #response = socket.recv(1024).decode('utf-8')

    # Stäng av anslutningen
print("Disconnected")