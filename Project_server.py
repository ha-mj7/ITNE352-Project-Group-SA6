import requests
import json
import threading
import socket
import ssl

#creating the ssl context
ssl_cont = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_cont.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

# creating a socket server
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as ss:
    ss.bind(("127.0.0.1", 1025))
    ss.listen(3)
    #asking the user for the airport code
    arr_icao = input('Enter the airport code: ')
    #the api requests parameters
    params = {
    'arr_icao': arr_icao,
    'limit': 100,
    'access_key': '639c95db4cd1525c7d6a83f5feb4803d'}
    #the api request
    api_data = requests.get('https://api.aviationstack.com/v1/flights', params)
    json_data = json.dumps(api_data.json(), indent= 2)
    fdata = api_data.json()
    #saving the data to the specified json file
    with open('SA6.json' , 'w') as f:
        result = f.write(json_data)
    #the thread function where the server recieves input from the client
    def Thread(sock_a, id):
        Cname = sock_a.recv(1024).decode('ascii')
        print('Client\'s name: {}'.format(Cname))
        
        try:
            while True:
                #making the json data searchable
                keys = fdata['data']
                choice = sock_a.recv(1024).decode('ascii')
                #if the user requests all arrived flights
                if choice.lower() in ['a','1']:
                    response_a = 'No arrived flights found\n'
                    for a in keys:
                        if a['arrival']['actual'] is not None:
                            if response_a == 'No arrived flights found\n':
                                response_a = '=======================All arrived flights=========================\n'
                            response_a += (
                                "-----------------------------------------\n"
                                f"Flight IATA code: {a['flight']['iata']}\n"
                                f"Departure airport: {a['departure']['airport']}\n"
                                f"Arrival time: {a['arrival']['actual']}\n"
                                f"Arrival terminal: {a['arrival']['terminal']}\n"
                                f"Arrival gate: {a['arrival']['gate']}\n"
                                "-----------------------------------------\n"
                            )
                    print('All arrived flights requested by {}'.format(Cname))
                    sock_a.sendall(response_a.encode('utf-8'))


    
                #if the user requests all delayed flights
                elif choice.lower() in ['b','2']:
                    response_b = 'No delayed flights found\n'
                    for b in keys:
                        if b['arrival']['delay'] is not None:
                            if b['flight']['codeshared'] is not None:
                                if response_b == 'No delayed flights found\n':
                                    response_b = '=======================All delayed flights=========================\n'
                                response_b += (
                                    "-----------------------------------------\n"
                                    f"Flight IATA code: {b['flight']['iata']}\n"
                                    f"Departure airport: {b['departure']['airport']}\n"
                                    f"Departure scheduled: {b['departure']['scheduled']}\n"
                                    f"Arrival estimated: {b['arrival']['estimated']}\n"
                                    f"Arrival terminal: {b['arrival']['terminal']}\n"
                                    f"Arrival delay: {b['arrival']['delay']}\n"
                                    f"Arrival gate: {b['arrival']['gate']}\n"
                                    "-----------------------------------------\n"
                                )
                    print('All delayed flights requested by {}'.format(Cname))
                    sock_a.sendall(response_b.encode('utf-8'))
                #if the user requests a particular flight using the flight IATA code
                elif choice.lower() in ['c', '3']:
                    sock_a.send('Please enter the flight IATA code: '.encode('ascii'))
                    response_c = 'No flights with this number found\n'
                    fli_iata = sock_a.recv(1024).decode('ascii')
                    for c in keys:
                        if c ['flight']['iata'] == fli_iata:
                            if response_c == 'No flights with this number found\n':
                                response_c = '=======================Flight information for IATA code:{}=========================\n'.format(fli_iata)
                            response_c += (
                                "---------------------------------------------------------\n"
                                f"Flight IATA code: {c['flight']['iata']}\n"
                                f"Departure airport: {c['departure']['airport']}\n"
                                f"Departure gate: {c['departure']['gate']}\n"
                                f"Departure terminal: {c['departure']['terminal']}\n"
                                f"Arrival airport: {c['arrival']['airport']}\n"
                                f"Arrival gate: {c['arrival']['gate']}\n"
                                f"Arrival terminal: {c['arrival']['terminal']}\n"
                                f"Arrival status: {c['flight_status']}\n"
                                f"departure scheduled: {c['departure']['scheduled']}\n"
                                f"Arrival scheduled: {c['arrival']['scheduled']}\n"
                                "----------------------------------------------------------\n"
                            )
                            #using the break statement to stop the loop since the flight has been found
                            break
                    print('Details of a particular flight requested by {}'.format(Cname))
                    sock_a.sendall(response_c.encode('utf-8'))
                #if the user wants to disconnect from the server
                elif choice.lower() in ['d','quit', '4']:
                        print('Disconnecting Client: {}'.format(Cname))
                        sock_a.send('Closing connection'.encode('ascii'))
                        sock_a.close()  
                        break
                #if the user enters an invalid choice
                else:
                    Invalid = (
                        "---------------------------------------------------------\n"
                        f">>>>>>>>>>>>>>>Invalid choice, try again<<<<<<<<<<<<<<<<\n"
                        "---------------------------------------------------------\n"
                    )
                    sock_a.send(Invalid.encode('ascii'))
        #if the client disconnects from the server not using the quit option
        except (ConnectionResetError, BrokenPipeError):
            print("Client {} disconnected.".format(Cname))
        finally:
            sock_a.close()


    #creating a list to store the threads
    my_threads=[]
    #creating a loop for threads so it can accept up to 5 clients
    while True:
        sock_a,sockname= ss.accept()
        try:
            #wrapping the client socket with SSL
            ssl_conn = ssl_cont.wrap_socket(sock_a, server_side=True)
            t = threading.Thread(target= Thread,args=(ssl_conn,len(my_threads)+1))
            print('New thread has been created for {}'.format(sockname[0]))
            my_threads.append(t)
            t.start()
        except ssl.SSLError as error:
            print(f"SSL error: {error}")
            sock_a.close()
