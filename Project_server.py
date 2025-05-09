import requests
import json
import threading
import time
import socket

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as ss:
    ss.bind(("127.0.0.1",777))
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
        while True:
            Cname = sock_a.recv(1024).decode('ascii')
            print('Client\'s name: {}'.format(Cname))
            choice = sock_a.recv(1024).decode('ascii')
            keys = fdata['data']
            if choice.lower() in ['a','1']:
                for a in keys:
                    if a['arrival']['actual'] is not None:
                        response_a = (
                            '-----------All arrived flights-----------\n'
                            f'Flight IATA code: {a['flight']['iata']}\n'
                            f'Departure airport: {a['departure']['airport']}\n'
                            f'Arrival time: {a['arrival']['actual']}\n'
                            f'Arrival terminal: {a['arrival']['terminal']}\n'
                            f'Arrival gate: {a['arrival']['gate']}\n'
                            '-----------------------------------------\n'
                        )
                    sock_a.send(response_a.encode('ascii'))
                
            
                        

            


         
    my_threads=[]

    while True:
        sock_a,sockname= ss.accept()
        t = threading.Thread(target= Thread,args=(sock_a,len(my_threads)+1))
        print('New thread has been created for {}'.format(sockname[0]))
        my_threads.append(t)
        t.start()
        if len(my_threads)> 5:
            break


