import os
import sys
import time
from dotenv import load_dotenv

# Configure stdout to support UTF-8 characters (like emojis) when printing in Windows terminal
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

# Load credentials from .env file
load_dotenv()

# Verify that the required Google API key exists in the environment
if not os.getenv("GOOGLE_API_KEY"):
    print("ERROR: GOOGLE_API_KEY not found. Add it to your .env file.")
    exit(1)

from agent import run_agent

# The evaluation questions to trace agent actions and responses
questions = [
    "Where is my order ORD-1002?",
    "Is there a cheaper alternative to the shoes I ordered in ORD-1001?",
    "Tell me about the laptops in your store",
    "Where is order ORD-9999?",
    "Do you have any wireless headphones?"
]

for idx, question in enumerate(questions):
    print(f"\n{'='*60}")
    print(f"Customer: {question}")
    # Run the graph loops and print final response
    print(f"Agent   : {run_agent(question)}")
    
    # Add a rate-limiting delay between questions (except the last one)
    if idx < len(questions) - 1:
        print("\n[Rate Limiter] Sleeping 22 seconds to respect Free Tier API limits...")
        time.sleep(22)

