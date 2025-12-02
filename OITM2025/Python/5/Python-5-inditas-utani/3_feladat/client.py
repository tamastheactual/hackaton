import networkx as nx
import pandas as pd 
import requests

# Start and finish nodes are hardcoded
start = 0
end = 35

# FakeWaze server:
url = 'http://localhost:8000/route'
number_of_requests = 101

# Send a request to the server
responses = []

for i in range(number_of_requests):
    response = requests.post(
        url,
        json={'start' : start,'end' : end}
        )
    responses.append(response)
    #print(response.json())

# Question: final shortest path
print(f'Az utolsó legrövidebb út hossza {response.json()["distance"]}')

print(f'Az utolsó legrövidebb útvonalak: {response.json()["paths"]}')

# Question: összesen hány különböző útvonal van a visszakapott útvonalak között?
routes = pd.DataFrame([path for a in responses for path in a.json()['paths']])
print(f'Az összesen visszakapott különböző útvonalak száma: {len(routes.drop_duplicates())}')