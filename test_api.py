import requests

# Define the API endpoint
url = "http://127.0.0.1:5000/predict"

# Replace with actual feature values (Ensure you provide 49 features)
sample_input = {
    "features": [0.5] * 49  # Example: Sending 49 values (Replace with real data)
}

# Send a POST request to the API
response = requests.post(url, json=sample_input)

# Print API response
print("Response from API:", response.json())
