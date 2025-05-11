import requests
import json
import threading
import socket

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as ss:
    ss.bind(("127.0.0.1", 1025))
    ss.listen(3)
    
    arr_icao = input('Enter the airport code:')
    params = {
    'arr_icao': arr_icao,
    'limit': 100,
    'access_key': '0e69ff7b13e782fd5508e69d9fd8eb2c'}

    api_data = requests.get('https://api.aviationstack.com/v1/flights', params)
    json_data = json.dumps(api_data.json(), indent= 2)
    fdata = api_data.json()

    with open('SA6.json' , 'w') as f:
        result = f.write(json_data)

    def Thread(sock_a, id):
        Cname = sock_a.recv(1024).decode('ascii')
        print('Client\'s name: {}'.format(Cname))
        
        try:
            while True:
                keys = fdata['data']
                choice = sock_a.recv(1024).decode('ascii')

                if choice.lower() in ['a','1']:
                    response_a = 'No arrived flights found\n'
                    for a in keys:
                        if a['arrival']['actual'] is not None:
                            if response_a == 'No arrived flights found\n':
                                response_a = ''
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
                    sock_a.sendall(response_a.encode('ascii'))


    
                #delayed flights
                elif choice.lower() in ['b','2']:
                    for b in keys:
                        if b['arrival']['delay'] is not None:
                            if b['flight']['codeshared'] is not None:
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
                            else:
                                response_b = 'No delayed flights found\n'
                    print('All delayed flights requested by {}'.format(Cname))
                    sock_a.sendall(response_b.encode('ascii'))

                elif choice.lower() in ['c', '3']:
                    sock_a.send('Please enter the flight number:'.encode('ascii'))
                    fli_num = sock_a.recv(1024).decode('ascii')
                    for c in fdata['data']:
                        if c ['flight']['number'] == fli_num:
                            response_c = (
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
                            break
                    print('Details of a particular flight requested by {}'.format(Cname))
                    sock_a.sendall(response_c.encode('ascii'))
                
                elif choice.lower() in ['d','quit', '4']:
                        print('Disconnecting Client: {}'.format(Cname))
                        sock_a.send('Closing connection'.encode('ascii'))
                        sock_a.close()  
                        break
                else:
                    sock_a.send('Invalid choice'.encode('ascii'))

        except (ConnectionResetError, BrokenPipeError):
            print("Client {} disconnected.".format(Cname))
        finally:
            sock_a.close()



    my_threads=[]

    while True:
        sock_a,sockname= ss.accept()
        t = threading.Thread(target= Thread,args=(sock_a,len(my_threads)+1))
        print('New thread has been created for {}'.format(sockname[0]))
        my_threads.append(t)
        t.start()
        if len(my_threads)> 5:
            print('Maximum number of clients reached')
            break