import requests



headers = {

  'Content-Type': 'application/json',

  'Authorization': 'Bearer Xa3gWHn0JNdMpjTpsUcEW3pCzgyx'

}



payload = {

    "BusinessShortCode": 174379,

    "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMxMTE2MDkxODM0",

    "Timestamp": "20231116091834",

    "TransactionType": "CustomerPayBillOnline",

    "Amount": 1,

    "PartyA": 254759633150,

    "PartyB": 174379,

    "PhoneNumber": 254759633150,

    "CallBackURL": "https://mydomain.com/path",

    "AccountReference": "CompanyXLTD",

    "TransactionDesc": "Payment of X" 

  }



response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = payload)

# print(response.text.encode('utf8'))
data =response.json()
print(data)