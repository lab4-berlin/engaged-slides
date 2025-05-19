# app/services/chatgpt_service.py
import openai
from flask import current_app
import base64

def analyze_with_chatgpt(file):
    openai.api_key = current_app.config['OPENAI_API_KEY']
    
    try:
        # Read the file content
        file_content = file.read()
        file_name = file.filename
        
        # Try to decode as text, if fails, use base64
        try:
            content_str = file_content.decode('utf-8')
        except UnicodeDecodeError:
            # For binary files, encode as base64
            content_str = f"[Binary file encoded in base64]: {base64.b64encode(file_content).decode('ascii')}"
        
        system_prompt = current_app.config['CHATGPT_PROMPT']
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"File name: {file_name}\n\nFile content:\n{content_str}"
                }
            ],
            max_tokens=4096
        )
        
        file.seek(0)  # Reset file pointer for potential further use
        return response['choices'][0]['message']['content']
    except Exception as e:
        raise Exception(f"Failed to analyze with ChatGPT: {str(e)}")