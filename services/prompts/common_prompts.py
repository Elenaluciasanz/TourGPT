from openai import OpenAI
from django.conf import settings
    
def chat_gpt(prompt: str) -> str:
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model = settings.MODEL,
            messages = [{"role": "user", "content": prompt}]
        )
        print(response)
        
        finish_reason = response.choices[0].finish_reason
        if finish_reason == "stop":
            return response.choices[0].message.content
        
        return ""

    except Exception as e:
        print("Error while connecting with de API")
        print(e)
        return ""
