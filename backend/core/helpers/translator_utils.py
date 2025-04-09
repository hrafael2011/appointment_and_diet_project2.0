

import requests
from django.conf import settings


class Translator:
    def __init__(self):
        self.api_key = settings.TRANSLATOR_API_KEY
        self.endpoint = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0"
        self.region = "eastus"  # Cambia según tu región

    def translate(self, text, target_language="en"):
        """
        Método para traducir texto utilizando Microsoft Translator API.
        """
        if not text:
            return ""

        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-type": "application/json",
            "Ocp-Apim-Subscription-Region": self.region,
        }
        params = {"to": target_language}
        body = [{"text": text}]

        # Debug
        print(f"Endpoint: {self.endpoint}")
        print(f"Headers: {headers}")
        print(f"Params: {params}")
        print(f"Body: {body}")

        response = requests.post(self.endpoint, headers=headers, params=params, json=body)
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        if response.status_code == 200:
            return response.json()[0]["translations"][0]["text"]
        else:
            raise ValueError(
                f"Error en la API de traducción: {response.status_code}, {response.text}"
            )
