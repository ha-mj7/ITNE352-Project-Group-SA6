import requests
import json
import threading
import time
import socket

ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.bind(("127.0.0.1",777))
ss.listen(3)

arr_icao = input('Enter the airport code:')

params = {
    'arr_icao': arr_icao,
    'limit': 100,
    'access_key': '0e69ff7b13e782fd5508e69d9fd8eb2c'
}

api_data = requests.get('https://api.aviationstack.com/v1/airports', params)
json_data = json.dumps(api_data.json(), indent= 2)

with open('SA6.json' , 'w') as f:
    f.write(json_data)



