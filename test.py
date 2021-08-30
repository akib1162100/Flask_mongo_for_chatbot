import requests

BASE_URL = 'http://127.0.0.1:5000/'
 
response = requests.post(BASE_URL+ 'user', {"name": 'AKIB', "password": '12345'})

# response = requests.get(BASE_URL+ 'user')
# response = requests.get(BASE_URL+ 'user/64002d09-de1c-4a57-b8b7-e615c150f4d1')
# response = requests.put(BASE_URL+ 'user/64002d09-de1c-4a57-b8b7-e615c150f4d1',{"name": 'AZIZUL', "password": '12345'})
# response = requests.delete(BASE_URL+ 'user/64002d09-de1c-4a57-b8b7-e615c150f4d1')
print(response.text)