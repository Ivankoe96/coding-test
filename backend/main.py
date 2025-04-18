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
    Accepts a user question and returns a data-aware or general response using the Gemini API (if configured).
    (Enhanced to handle both data-specific and general questions)
    """
    print("\n--- AI Endpoint Called (Data-Aware + General) ---") # Add this line

    body = await request.json()
    user_question = body.get("question", "")

    print(f"Received question: '{user_question}'") # Add this line

    # Check if the Gemini client was configured successfully
    if not genai_client_configured:
        print("AI endpoint called but client not configured.")
        print("--- End AI Endpoint ---") # Add this line
        return {"answer": "AI service is currently unavailable (API key missing or configuration failed)."}

    if not user_question:
         print("No question provided.") # Add this line
         print("--- End AI Endpoint ---") # Add this line
         return {"answer": "Please provide a question."}

    # --- Data Retrieval Logic (Basic Keyword Matching) ---
    context_data = []
    user_question_lower = user_question.lower()

    # Search through sales representatives and their deals/clients
    for rep in DUMMY_DATA.get("salesReps", []):
        rep_name_lower = rep.get("name", "").lower()
        rep_role_lower = rep.get("role", "").lower()
        rep_region_lower = rep.get("region", "").lower()

        # Check if rep name, role, or region is in the question
        if rep_name_lower in user_question_lower or \
           rep_role_lower in user_question_lower or \
           rep_region_lower in user_question_lower:
            # If a sales rep is mentioned, add their relevant details to context
            # Avoid adding the entire representative object multiple times if they appear in multiple matches
            if rep not in context_data:
                 context_data.append(rep)

        # Also check if any client names mentioned in deals are in the question
        for deal in rep.get("deals", []):
             deal_client_lower = deal.get("client", "").lower()
             deal_status_lower = deal.get("status", "").lower() # Might also check status keywords
             if deal_client_lower in user_question_lower:
                  # If a client is mentioned in a deal, add that specific deal and the rep info
                  deal_context = {"deal": deal, "salesRepName": rep.get("name")} # Include rep name with deal
                  if deal_context not in context_data:
                      context_data.append(deal_context)
                  # Also make sure the rep is added if not already
                  if rep not in context_data:
                       context_data.append(rep)


    # --- Conditional Prompt Augmentation ---
    # Decide whether to include data context based on if anything was found
    if context_data:
        # If relevant data was found, format it and build a data-aware prompt
        context_string = json.dumps(context_data, indent=2) # Convert found data to JSON string

        system_instruction = (
            "You are an AI assistant knowledgeable about sales data. "
            "Answer the user's question based ONLY on the following sales data context if possible. "
            "If the question cannot be answered from the data provided, state that you cannot find relevant information in the provided data. "
            "Do not use outside knowledge to answer questions about the specific sales data."
        )

        augmented_prompt = f"{system_instruction}\n\nSales Data Context:\n{context_string}\n\nUser Question: {user_question}\n\nAnswer:"
        print(f"--- Relevant data found. Sending data-aware prompt ---") # Add this line
        print(f"Augmented Prompt (partial):\n{augmented_prompt[:500]}...") # Print start of prompt for debugging

    else:
        # If NO relevant data was found, send only the user's question as a general prompt
        augmented_prompt = user_question
        print(f"--- No relevant data found. Sending general prompt ---") # Add this line
        print(f"General Prompt: {augmented_prompt}") # Print the prompt


    # --- Call the Gemini API with the Augmented/General Prompt ---
    try:
        # Send the chosen prompt (either data-aware or general)
        response = generation_model.generate_content(augmented_prompt)
        print("Successfully received response from Gemini.") # Add this line

        # Access the generated text from the response.
        # Handle potential cases where the model might not return text
        if response and response.text:
             ai_answer = response.text
        else:
             # Handle cases where the model didn't generate text (e.g., blocked for safety)
             print("Gemini did not return text response.")
             ai_answer = "The AI did not return a valid text response."
             if response.candidates:
                 for candidate in response.candidates:
                     if candidate.finish_reason:
                         ai_answer += f" Finish reason: {candidate.finish_reason}."
                     if candidate.safety_ratings:
                          ai_answer += " Safety ratings present." # Check details if needed


        print(f"Gemini response text (partial): {ai_answer[:200]}...") # Print start of answer
        print("--- End AI Endpoint ---") # Add this line


        return {"answer": ai_answer}

    except Exception as e:
        print(f"\n--- Error calling Gemini API ---") # Add this line
        print(f"Exception details: {e}")          # Print the exception 'e'
        print("--- End AI Endpoint ---") # Add this line
        # Return a user-friendly error message to the frontend
        return {"answer": f"Error getting response from AI: {e}"}

# Add flush at the end for debugging prints
import sys
sys.stdout.flush()
sys.stderr.flush()


# Existing if __name__ == "__main__": block
if __name__ == "__main__":
    # This block is mainly for running the script directly.
    # When using `uvicorn main:app --reload`, the code outside functions/if blocks runs on reload.
    # The API key loading and configuration needs to be outside this block to work with --reload.
    print("main.py script executed directly.") # You might not see this with --reload
    pass # Uvicorn command handles server startup