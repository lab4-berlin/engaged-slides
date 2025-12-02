import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
    AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ALLOWED_EXTENSIONS = {'pdf', 'ppt', 'pptx', 'txt'}
    CHATGPT_PROMPT = os.getenv('CHATGPT_PROMPT', 'Please analyze this document and provide 3 multiple choice questions for students to see if they follow the lecture, make it visually nice as html')
