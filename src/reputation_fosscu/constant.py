import os
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_API_TOKEN = os.getenv("AIRTABLE_API_TOKEN")
