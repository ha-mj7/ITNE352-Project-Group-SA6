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
        choice = sock_a.recv(1024).decode('ascii')
        try:
            while True:
                keys = fdata['data']

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
                    print('All arrived flights:')
                    sock_a.send(response_a.encode('ascii'))


    
                #delayed flights
                elif choice.lower() in ['b','2']:
                    response_b = 'No delayed flights found\n'
                    for b in keys:
                        if b['arrival']['delay'] is not None:
                            if b['flight']['codeshared'] is not None:
                                if response_b == 'No delayed flights found\n':
                                    response_b = ''
                                response_b += (
                                    "-----------------------------------------\n"
                                    f"Fli-Iata: {b['flight']['iata']}\n"
                                    f"Dep-airport: {b['departure']['airport']}\n"
                                    f"Dep-scheduled: {b['departure']['scheduled']}\n"
                                    f"Arr-estimated: {b['arrival']['estimated']}\n"
                                    f"Arr-terminal: {b['arrival']['terminal']}\n"
                                    f"Arr_delay: {b['arrival']['delay']}\n"
                                    f"Arr-gate: {b['arrival']['gate']}\n"
                                    "-----------------------------------------\n"
                                )
                    print('All delayed flights:')
                    sock_a.send(response_b.encode('ascii'))

                elif choice.lower() in ['c', '3']:
                    ask = 'Please enter the flight number >>>'
                    sock_a.sendall(ask.encode('ascii'))
                    fli_num = sock_a.recv(1024).decode('ascii')
                    response_d = 'Sorry, no data found for this Flight number :('
                    for c in fdata['data']:
                        if c ['flight'].get('number') == fli_num:
                            response_d = (
                                "---------------------------------------------------------\n"
                                f"Fli_iata: {c['flight'].get('iata', 'N/A')}\n"
                                f"Dep_airport: {c['departure'].get('airport', 'N/A')}\n"
                                f"Dep_gate: {c['departure'].get('gate', 'N/A')}\n"
                                f"Dep_terminal: {c['departure'].get('terminal', 'N/A')}\n"
                                f"Arr_airport: {c['arrival'].get('airport', 'N/A')}\n"
                                f"Arr_gate: {c['arrival'].get('gate', 'N/A')}\n"
                                f"Arr_terminal: {c['arrival'].get('terminal', 'N/A')}\n"
                                f"Fli_status: {c.get('flight_status', 'N/A')}\n"
                                f"Dep_scheduled: {c['departure'].get('scheduled', 'N/A')}\n"
                                f"Arr_scheduled: {c['arrival'].get('scheduled', 'N/A')}\n"
                                "----------------------------------------------------------\n"
                            )
                            break
                    print('Details of a particular flight')
                    sock_a.send(response_d.encode('ascii'))
                
                elif choice.lower() in ['d','quit', '4']:
                        print('Disconnecting Client: ', Cname)
                        sock_a.send('Closing connection'.encode('ascii'))
                        sock_a.close()  
                        break
                else:
                    sock_a.send('Invalid choice'.encode('ascii'))

        except (ConnectionResetError, BrokenPipeError):
            print("Client {} disconnected unexpectedly.".format(Cname))
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