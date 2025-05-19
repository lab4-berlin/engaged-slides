from openai import OpenAI
from flask import current_app
import base64

def truncate_content(content, max_chars=10000):
    """Truncate content to a maximum number of characters"""
    if len(content) > max_chars:
        return content[:max_chars] + "\n...(content truncated due to length)..."
    return content

def analyze_with_chatgpt(file):
    client = OpenAI(api_key=current_app.config['OPENAI_API_KEY'])
    
    try:
        # Read the file content
        file_content = file.read()
        file_name = file.filename
        
        # Try to decode as text, if fails, use base64
        try:
            content_str = file_content.decode('utf-8')
            # Truncate content to avoid token limit
            content_str = truncate_content(content_str)
        except UnicodeDecodeError:
            # For binary files, encode as base64 and truncate
            base64_str = base64.b64encode(file_content).decode('ascii')
            content_str = f"[Binary file encoded in base64]: {truncate_content(base64_str)}"
        
        system_prompt = current_app.config['CHATGPT_PROMPT']
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",  # Latest GPT-4 Turbo model
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
            max_tokens=16384  # Maximum possible output tokens for GPT-4
        )
        
        file.seek(0)  # Reset file pointer for potential further use
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Failed to analyze with ChatGPT: {str(e)}")