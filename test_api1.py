import requests

url = "http://127.0.0.1:5000/chatbot"
data = {"message": "My app keeps crashing when I try to update!"}

response = requests.post(url, json=data)
print("Response from API:", response.json())
