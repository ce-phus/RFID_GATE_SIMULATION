import requests
import base64

# Mpesa API Credentials
consumer_key='PEtuGJp8Pm6TMnOizMbL43NB3mfHvUiH'
consumer_secret='EAZwU23AYhB8HwAi'
shortcode='174379'
lipa_na_mpesa_online_pass_key="MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMxMTE2MDkxODM0"

# M-pesa API endpoints
auth_url='https://sandbox.safaricom.co.ke/oauth/v1/generate'
lipa_na_mpesa_online_url='https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

# Authenticate with M-pesa API
def get_access_token():
    auth=base64.b64encode(f"{consumer_key}: {consumer_secret}".encode()).decode()
    headers={"Authorization": f"Basic{auth}"}
    response= requests.get(auth_url, headers=headers)
    data= response.json
    return data.get('access_token')

# Initiate Lipa na Mpesa Online Payment
def lipa_na_mpesa_payment(access_token):
    headers={
        'Authorization': f"Bearer{access_token}",
        "Content-Type": "application/json"
    }
    payload= {
        "BusinessShortCode": shortcode,
        "Password": lipa_na_mpesa_online_pass_key,
        "Timestamp": "20231116091834",
        "TransactionType": "CustomerPaybillOnline",
        "Amount": "100",
        "PartyA": "254759633150",
        "PartyB": shortcode,
        "PhoneNUmber": "0759633150",
        "CallBackUrl": "",
        "AccountReference": "123456",
        "TransactionDesc": "Payment for items" 
    }
    response= requests.post(lipa_na_mpesa_online_url, json=payload, headers=headers)
    data= response.json()
    return data



