from typing import Dict
from openai import OpenAI
from google.adk.agents import Agent  # Make sure this is a valid path in your env
from google.adk.models.registry import LLMRegistry
import datetime
from dotenv import load_dotenv
import os

# --- Load environment variables ---
load_dotenv()

# --- OpenAI Client ---
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  # Make sure you have this in your .env file
)

# --- Tool Definition ---

def fix_code(code: str) -> dict:
    """
    Uses GPT-4.1 to fix and explain the given code.
    """
    print("Tool: Fixing code...")

    prompt = (
        "You are an expert software engineer. "
        "The user provided code may contain bugs, bad practices, or formatting issues. "
        "Please fix the code and explain the improvements made.\n\n"
        f"Code:\n{code}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4.1",  # Use "gpt-4" or "gpt-4-0613", not "gpt-4.1" (not a valid model id)
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1024,
            top_p=1
        )

        fixed_code = response.choices[0].message.content

        return {
            "status": "success",
            "fixed_code": fixed_code,
            "message": "Code analyzed and improved successfully."
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to analyze code: {str(e)}"
        }

# --- Agent Definition ---



root_agent = Agent(
    name="code_fixer",
    model="gemini-1.5-flash-001",  # Ensure model supports function calling
    description="Agent to answer questions about the coding",# that fixes broken or poorly written code and explains the changes.
    instruction=(
        "You are a helpful agent"
        "Use the 'fix_code' tool to analyze and fix the code. "
        "Provide a corrected version of the code and explain the changes clearly. "
        "If there are issues with the code, inform the user accordingly. "
    ),
    tools=[fix_code],
)
