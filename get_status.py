import requests


response = requests.get(url='http://10.0.0.220:32149', headers={'command': 'get status', 'User-Agent': 'AnyLog/1.23'})
response.raise_for_status()
print(response.text)
