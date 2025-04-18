from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json

# --- New Imports for Environment Variables and Gemini ---
import os # Import os module to access environment variables
from dotenv import load_dotenv # Import load_dotenv
import google.generativeai as genai # Import the google.generativeai library
# --- End New Imports ---


app = FastAPI()

# --- Load Environment Variables and Configure Gemini ---
# Load environment variables from .env file (make sure .env is in the project root, coding-test)
# This function looks for a .env file in the current directory and its parents.
load_dotenv()

# Configure the Gemini API with your key from environment variables
# Make sure you have a file named .env in your project root with a line like GEMINI_API_KEY=YOUR_API_KEY
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    print("\nError: GEMINI_API_KEY not found in environment variables or .env file.")
    print("Please create a .env file in the project root with GEMINI_API_KEY=YOUR_API_KEY.")
    print("The AI endpoint will not be functional without the API key.\n")
    genai_client_configured = False
else:
    try:
        genai.configure(api_key=gemini_api_key)
        # Optional: You can uncomment the lines below to list models when the server starts
        # print("Google Generative AI configured. Available models:")
        # for model in genai.list_models():
        #     print(f"- {model.name}")

        genai_client_configured = True
        # Select the model you want to use. 'gemini-2.0-flash' is a common choice for text generation.
        # Check Google's documentation for available model names and their capabilities.
        generation_model_name = 'gemini-2.0-flash' # <<<--- CONFIRM THIS MODEL NAME IS SUITABLE/AVAILABLE
        generation_model = genai.GenerativeModel(generation_model_name)
        print(f"Gemini model '{generation_model_name}' selected for generation.")

    except Exception as e:
        print(f"\nError configuring Google Generative AI: {e}\n")
        print("Please check your GEMINI_API_KEY and ensure it's valid.")
        genai_client_configured = False
# --- End Load Environment Variables and Configure Gemini ---


# Existing CORS Middleware - MODIFIED TO ALLOW "POST" METHOD
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows your frontend origin
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # <<<--- CHANGED TO ALLOW GET AND POST
    allow_headers=["*"],  # Allows all headers (you can be more specific if needed)
)


# Existing Load dummy data (ensure path is correct relative to main.py)
# If main.py is in 'backend', and dummyData.json is in the root, "../dummyData.json" is correct.
dummy_data_path = "../dummyData.json"
DUMMY_DATA = {} # Initialize as empty dictionary
try:
    with open(dummy_data_path, "r") as f:
        DUMMY_DATA = json.load(f)
    print(f"Successfully loaded dummy data from {dummy_data_path}")
except FileNotFoundError:
    print(f"Error: dummyData.json not found at {dummy_data_path}")
    print("Sales data endpoint will return empty results.")
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {dummy_data_path}")
    print("Sales data endpoint may return incorrect results.")


@app.get("/api/sales-reps")
def get_data():
    """
    Returns the salesReps data from dummyData.json.
    """
    # Return the value associated with the "salesReps" key, or an empty list if the key is missing or DUMMY_DATA is empty
    return DUMMY_DATA.get("salesReps", [])


# Existing POST endpoint - MODIFIED TO CALL GEMINI API
@app.post("/api/ai")
async def ai_endpoint(request: Request):
    """
    Accepts a user question and returns a response using the Gemini API (if configured).
    """
    body = await request.json()
    user_question = body.get("question", "")

    # Check if the Gemini client was configured successfully
    if not genai_client_configured:
        print("AI endpoint called but client not configured.")
        return {"answer": "AI service is currently unavailable (API key missing or configuration failed)."}

    if not user_question:
         return {"answer": "Please provide a question."}

    try:
        # Call the Gemini API
        # This sends the user's question directly to the LLM.
        # For a more advanced bonus (RAG), you would add context from DUMMY_DATA
        # related to the user_question before sending the prompt to the LLM.
        print(f"Sending question to Gemini: {user_question}")
        response = generation_model.generate_content(user_question)

        # Access the generated text from the response.
        # The recommended way is response.text. Be aware this can raise an exception
        # if the model doesn't return text or has safety issues.
        ai_answer = response.text
        print("Received response from Gemini.")

        return {"answer": ai_answer}

    except Exception as e:
        print(f"\nError calling Gemini API: {e}\n")
        # Return a user-friendly error message to the frontend
        return {"answer": f"Error getting response from AI: {e}"}


# Existing if __name__ == "__main__": block
if __name__ == "__main__":
    # This block is mainly for running the script directly.
    # When using `uvicorn main:app --reload`, the code outside functions/if blocks runs on reload.
    # The API key loading and configuration needs to be outside this block to work with --reload.
    print("main.py script executed directly.") # You might not see this with --reload
    pass # Uvicorn command handles server startup