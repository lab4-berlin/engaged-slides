# app/services/chatgpt_service.py
import openai
from flask import current_app

def analyze_with_chatgpt(file_path):
    openai.api_key = current_app.config['OPENAI_API_KEY']
    
    try:
        # Here you would need to implement the logic to read the file from S3
        # and send its contents to ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": current_app.config['CHATGPT_PROMPT']},
                {"role": "user", "content": f"Analyze the document at: {file_path}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Failed to analyze with ChatGPT: {str(e)}")