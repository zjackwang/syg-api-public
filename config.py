import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)
# enable sessions

# MongoClient key
mongo_key = os.getenv("MONGO_KEY")

# API Keys
api_key = os.getenv("PUBLIC_API_PUBLIC_KEY")
secret_key = os.getenv("PUBLIC_API_SECRET_KEY")
