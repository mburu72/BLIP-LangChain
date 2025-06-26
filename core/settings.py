import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    G_A_K = os.getenv('GOOGLE_API_KEY')

settings = Settings()