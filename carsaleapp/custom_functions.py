import requests
from django.conf import settings
from celery import shared_task
from carsaleapp.models import NewUser


def send_otp(phone_number, message):
    headers = {"Authorization": settings.WHATSAPP_API_TOKEN}
    payload = {"messaging_product": "whatsapp",
               "recipient_type": "individual",
               "to": phone_number,
               "type": "template",
               "template":
                   {
                       "name": "otp",
                       "language":
                           {
                               "code": "az"
                           },
                       "components":
                           [
                               {
                                   "type": "body",
                                   "parameters":
                                       [
                                           {
                                               "type": "text",
                                               "text": message
                                           }
                                       ]
                               },
                               {
                                   "type": "button",
                                   "sub_type": "url",
                                   "index": "0",
                                   "parameters": [
                                       {
                                           "type": "text",
                                           "text": message
                                       }
                                   ]
                               }
                           ]
                   }
               }
    response = requests.post(settings.WHATSAPP_API_URL, headers=headers, json=payload)
    return response.json()


@shared_task
def reset_otp_attempts():
    NewUser.objects.all().update(otp_attempts=3)
