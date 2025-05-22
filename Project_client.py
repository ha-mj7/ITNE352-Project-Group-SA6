import socket
import ssl

#function to receive all data from the socket assuring that the data is not cut off in the process
def recv_all(sock, buffer=4096):
    data = b''
    while True:
        chunck = sock.recv(buffer)
        data += chunck
        if len(chunck) < buffer:
            break
    return data.decode('utf-8')

#ssl context creation
ssl_cont = ssl.create_default_context()
ssl_cont.check_hostname = False
ssl_cont.verify_mode = ssl.CERT_NONE


#creating the client socket
address = ("127.0.0.1", 1025)
Cname = input('Enter your name: ')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cs:
    cs.connect(address)

    #wrapping the socket with ssl
    ssl_sock = ssl_cont.wrap_socket(cs, server_hostname=address[0])
    ssl_sock.sendall(Cname.encode('ascii'))  
    #showing the user the available options
    while True:
        print("\nOptions:")
        print("a. Show all arrived flights")
        print("b. Show all delayed flights")
        print("c. Search for a particular flight")
        print("d. Quit connection")
        #Asking the user for to enter the option
        choice = input("Choose one of the options above: ").strip()
        if not choice:
            continue
        #sending the inut to the server
        ssl_sock.send(choice.encode('ascii'))
        #if the user wants to quit the connection to the server
        if choice in ['d', '4', 'quit']:
            print("============Disconnecting from server============")
            break
        #asking the user for the flight IATA code when entering option c
        if choice in ['c','3']:
            reply = recv_all(ssl_sock)
            print(reply)
            fli_iata = input().upper().strip()
            ssl_sock.send(fli_iata.encode('ascii'))
        #receiving the server's response
        response = recv_all(ssl_sock) 
        print(response)