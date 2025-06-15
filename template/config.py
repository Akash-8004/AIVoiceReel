import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="config.env")  # or just load_dotenv() if the file is named `.env`

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
