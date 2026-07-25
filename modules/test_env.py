from dotenv import load_dotenv
import os

load_dotenv()

print("APP ID:", os.getenv("ADZUNA_APP_ID"))
print("APP KEY:", os.getenv("ADZUNA_APP_KEY"))