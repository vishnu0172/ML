# Gemini API Starter

This project is a small Python app that sends a prompt to Google's Gemini API and prints the model response plus a few usage/latency details.

## Setup

1. Create and activate a virtual environment if needed.
2. Install dependencies:

   python3 -m pip install -r requirements.txt

3. Add your API key in a `.env` file based on `.env.example`:

   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL=gemini-3.8-flash

## Run

python3 firstapi.py

Optional custom prompt:

python3 firstapi.py --prompt "Write a short summary of machine learning."
