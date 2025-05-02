import requests
import base64

# Example function to send POST request to an endpoint
def test_create_user(url, user_data):
    headers = {
    'Authorization': 'Token 8ac402c68477145534f13ab97bae99899290ff85'
    }
    headers2 = {
        'Authorization': f'Basic {base64.b64encode(b"testteacher:securepassword").decode("utf-8")}'
    }
    response = requests.get(url, json=user_data, headers=headers)
    print("Response Content:", response.content)
    return response.json(), response.status_code

# Example usage
url = "http://localhost:8000/api/data/overview/"


user_data = {
  "student": 1,  
  "month": "Aprel 2025",
  "amount": "200000.00",
  "is_paid": True,
  "payment_date": "2025-04-05",
  "course": 3
}


headers = {
    'Authorization': 'Token 785a368f2764db1ab02a2936996675959b9a6736'
}

response_data, status_code = test_create_user(url, user_data)
print("Response Data:", response_data)
print("Status Code:", status_code)
