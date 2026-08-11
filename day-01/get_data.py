import requests
      
url="https://fake-json-api.mock.beeceptor.com/companies"
response=requests.get(url=url)

print(response.json())

