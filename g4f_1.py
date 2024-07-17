import requests

class ChatGPT4o:
    def __init__(self, provider_url):
        self.provider_url = provider_url

    def create(self, prompt):
        response = requests.post(self.provider_url, json={"prompt": prompt})
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Ошибка при запросе к провайдеру"}
