import requests
from django.conf import settings

api_key = settings.TWO_FACTOR_API_KEY


def send_authentication_otp(mobile_number):
    try:
               
        url = f"http://2factor.in/API/V1/{api_key}/SMS/{mobile_number}/AUTOGEN/OTP1"

        payload = ""
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request(
            "GET", url, data=payload, headers=headers)
        return response

    except Exception as e:
        return e


def verify_otp(session_id, otp):
    try:
        url = f"http://2factor.in/API/V1/{api_key}/SMS/VERIFY/{session_id}/{otp}"

        payload = ""
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("GET", url, data=payload, headers=headers)
        return response

    except Exception as e:
        return e
