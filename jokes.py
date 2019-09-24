import requests
resp=requests.get('https://official-joke-api.appspot.com/random_ten')

dir(resp)
resp.json()

print(resp.json()[0]['setup'])
print(resp.json()[0]['punchline'])
