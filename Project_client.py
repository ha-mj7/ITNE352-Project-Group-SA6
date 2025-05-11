import socket

address = ("127.0.0.1", 1025)
Cname = input('Enter your name: ')
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as cs:
    cs.connect(address)
    cs.send(Cname.encode('ascii'))

    while True:
        print('a. Show all arrived flights')
        print('b. Show all delayed flights')
        print('c. Search for a particular flight')
        print('d. Quit connection')

        choice = input("choose the option you need: ")
        cs.send(choice.encode('ascii'))

        if choice.lower() in ['c','3']:
            reply = cs.recv(1024).decode('ascii')
            print(reply)
            fli_num = input()
            cs.send(fli_num.encode('ascii'))

        response = cs.recv(2024).decode('ascii')
        print(response)
        
        if choice.lower() in ['d', '4', 'quit']:
            break


