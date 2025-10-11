# src/project/workflow/API/config.py
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

print(f"DEBUG: SECRET_KEY cargada (debería ser algo diferente a None): {SECRET_KEY}")
