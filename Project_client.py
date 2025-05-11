import socket


def recv_all(sock, buffer=4096):
    data = b''
    while True:
        chunck = sock.recv(buffer)
        data += chunck
        if len(chunck) < buffer:
            break
    return data.decode('ascii')

address = ("127.0.0.1", 1025)
Cname = input('Enter your name: ')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cs:
    cs.connect(address)
    cs.sendall(Cname.encode('ascii'))  

    while True:
        print("\nOptions:")
        print("a. Show all arrived flights")
        print("b. Show all delayed flights")
        print("c. Search for a particular flight")
        print("d. Quit connection")

        choice = input("Choose one of the options above: ").strip()
        if not choice:
            continue

        cs.send(choice.encode('ascii'))

        if choice in ['d', '4', 'quit']:
            print("++++++Disconnecting from server++++++")
            break

        if choice in ['c','3']:
            reply = recv_all(cs)
            print(reply)
            fli_num = input().strip()
            cs.send(fli_num.encode('ascii'))

        response = recv_all(cs) 
        print(response)