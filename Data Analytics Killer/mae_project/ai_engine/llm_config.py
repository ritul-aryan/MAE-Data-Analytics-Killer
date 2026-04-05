import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from the .env file securely
load_dotenv()

# Fetch the API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("🚨 GEMINI_API_KEY is missing. Please check your .env file.")

# Initialize the Gemini 2.5 Flash model
# We set temperature=0 because we want deterministic, highly reliable code
# generation for the Data Janitor, not creative hallucinations.
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # <--- THIS IS THE MAGIC FIX
    temperature=0,
    google_api_key=GEMINI_API_KEY
)

print("✅ Gemini 2.5 Flash initialized successfully.")