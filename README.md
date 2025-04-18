# Coding Challenge: Sales Dashboard with Next.js & FastAPI

## Overview
Your task is to build a simple, full-stack application featuring:
1. **Next.js** as the frontend framework.
2. **FastAPI** as the backend API layer.
3. **Dummy JSON Data** (provided) with sales-related information.

You will parse the provided **`dummyData.json`** and render its nested structures in a user-friendly interface. Optionally, you may include a simple AI feature as a bonus.

---

## Requirements

1. **Data Rendering (Required)**
   - The backend should serve the data from `dummyData.json` via a REST endpoint (e.g., `/api/sales-reps`).
   - The frontend must fetch this data asynchronously and display it in a meaningful way (e.g., a list of sales representatives, their deals, skills, etc.).
   - Demonstrate handling of nested JSON structures. For example, you might display each sales rep’s deals, status, and client details.

2. **UI/UX (Required)**
   - Use **Next.js** to implement at least one page that renders the fetched data.
   - Provide a basic, intuitive UI for viewing the sales reps’ information (e.g., deals, clients).
   - Show a loading state while data is being fetched, and handle potential errors gracefully.

3. **Backend API (Required)**
   - Use **FastAPI** to create an endpoint that returns the JSON data.
   - Implement CORS if needed, so the Next.js app can successfully request data from the FastAPI server.
   - Ensure your API is well-structured and documented (e.g., make use of FastAPI’s automatic docs or docstrings).

4. **Bonus: AI Feature (Optional)**
   - Add an endpoint (e.g., `/api/ai`) that accepts user input (e.g., a question) and returns a generated or placeholder response.
   - Integrate this into the frontend with a simple form or input field where the user can type a question and view the AI’s response.
   - The AI logic can be **mocked** or **rule-based** if you do not wish to integrate an actual AI service. If you prefer, you may call any AI API you have access to (such as OpenAI, etc.).

---

## Using Free LLM APIs

Various Large Language Model (LLM) providers offer free or trial APIs. Here are some examples:

- **Google Gemini API**  
  Google provides a free tier for the Gemini model API with certain usage limits. You can generate an API key and refer to the official documentation for details.

- **Meta’s Llama 2**  
  Meta has open-sourced the Llama 2 model, which can be used for both commercial and research purposes at no cost. You can apply for access and download the model from their official website.

- **Upstage’s Solar**  
  Upstage provides a free API trial for its Solar LLM, showcasing its powerful features. Refer to their official documentation or blog for more information.

Additionally, IBM, Study space, “Stibee,” and others may offer free or trial-based LLM APIs.

> **LangChain**  
> LangChain is a framework that supports integrating multiple LLMs in a unified way. You can check LangChain’s list of integrations to see which models are supported and choose the one that suits your project.

Using these free or trial options can help you add an AI chatbot or similar functionality to your project without significant costs.

---

## Submission Instructions (Fork)

1. **Fork This Repository**  
   - In the top-right corner of this repo page, click on the “Fork” button to create your own copy of the project under your GitHub account.

2. **Clone Your Fork**  
   - After forking, clone your forked repository to your local machine:
     ```bash
     git clone https://github.com/<your-username>/<repo-name>.git
     ```
3. **Implement Your Solution**  
   - Work on your solution locally (both frontend and backend as described below).  
   - Commit your changes in a clean, organized manner.


- Then, go to your forked repository on GitHub and Provide a link to your forked repository and emailing it to us
- Provide a clear description of what you’ve implemented or any notable design choices.

---

## Deliverables

- **Forked Repository**: Contains all changes, with commits reflecting your development process.

---

## Evaluation Criteria

1. **Code Quality & Organization**  
   - Readability, maintainability, and modularity.  
   - Clear separation of concerns between frontend and backend.

2. **Data Handling**  
   - Ability to fetch, parse, and display nested data structures.  
   - Proper use of asynchronous operations and error handling.

3. **UI/UX**  
   - Clean, intuitive interface.  
   - Demonstration of loading states and helpful user feedback.

4. **AI Integration (Bonus)**  
   - Creativity and correctness of the AI feature.  
   - Proper request/response handling on both frontend and backend.

5. **Documentation**  
   - Clarity in the instructions to set up and run the project.  
   - Brief explanation of design choices and potential improvements.

---

## Getting Started

1. **Clone or Download** this repository (or fork it, as described above).
2. **Backend Setup**  
   - Navigate to the `backend` directory.  
   - Create a virtual environment (optional but recommended).  
   - Install dependencies:  
     ```bash
     pip install -r requirements.txt
     ```  
   - Run the server:  
     ```bash
     uvicorn main:app --host 0.0.0.0 --port 8000 --reload
     ```  
   - Confirm the API works by visiting `http://localhost:8000/docs`.

3. **Frontend Setup**  
   - Navigate to the `frontend` directory.  
   - Install dependencies:  
     ```bash
     npm install
     ```  
   - Start the development server:  
     ```bash
     npm run dev
     ```  
   - Open `http://localhost:3000` to view your Next.js app.

4. **Data**  
   - The file `dummyData.json` is located in the `backend` directory (or wherever you place it).
   - Adjust your API endpoint and frontend calls if you use different paths or filenames.

5. **AI Feature (If Implemented)**  
   - Add a POST endpoint to handle AI requests, for example `/api/ai`.  
   - In the frontend, create a simple form to collect user questions and display the returned answer.
   - Feel free to use any **free or trial LLM API** mentioned above or implement a rule-based approach.

6. **Tips for Completion**
   - **Start Small**: Fetch the data, display it, then expand to more complex UI or AI functionality.
   - **Testing**: You may add unit or integration tests if time permits.
   - **UI Libraries**: Feel free to use any UI library or styling approach (Tailwind, CSS modules, etc.) if desired.
   - **Extensions**: You can incorporate charts, filters, or sorting to demonstrate extra skills.

---

**Good luck, and have fun building your Sales Dashboard!**


# InterOpera Coding Test Solution - Ivan Koe

## Project Description

This project is a solution to the InterOpera coding test. It consists of a backend API built with FastAPI (Python) and a frontend application built with Next.js (React). The application displays sales performance data for representatives and includes an optional AI endpoint feature integrated with the Google Gemini API.

## Features Implemented

* **Required:**
    * Backend API (`/api/sales-reps`) serving sales data from `dummyData.json`.
    * Frontend display of sales representatives.
    * Display of nested deal information for each representative.
    * Display of the sales representative's **Region** on the frontend.

* **Optional AI Bonus:**
    * Backend API endpoint (`/api/ai`) that accepts a user question via POST request.
    * Integration with the **Google Gemini API** to generate responses.
    * **Data-Aware AI:** The AI attempts to answer questions based on the `dummyData.json` content (basic RAG implementation via keyword matching and prompt augmentation). If the question is not related to the data, it answers using its general knowledge.


## Design Notes and Choices

* **Overall Layout:** The layout is a simple top-down flow with sales data above and the AI interaction section below.
* **Data Display:** Sales representatives are displayed in a grid layout for easy viewing. Nested deals for each rep are listed clearly below their name. The representative's region from the `dummyData.json` was also included.
* **Basic UI:** The UI uses clear headings and distinct sections for intuitive navigation.

## Technologies Used

* **Backend:**
    * Python
    * FastAPI
    * Uvicorn
    * `python-dotenv`
    * `google-genai`
* **Frontend:**
    * Node.js
    * npm
    * React
    * Next.js

## Setup and Installation

Follow these steps to get the project running locally:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Ivankoe96/coding-test
    cd coding-test
    ```
   

2.  **Google Gemini API Key:**
    * Obtain a Google Gemini API key from [Google AI Studio](https://aistudio.google.com/).
    * Create a file named `.env` in the **root directory** of the cloned `coding-test` project folder.
    * Add the following line to the `.env` file, replacing `YOUR_API_KEY_HERE` with your actual Gemini API key:
        ```env
        GEMINI_API_KEY=YOUR_API_KEY_HERE
        ```
    * *(Note: The `.env` file is ignored by Git for security)*

3.  **Backend Setup:**
    * Open a terminal window and navigate to the `backend` directory:
        ```bash
        cd backend
        ```
    * (Windows) Create a Python Virtual Environment:
        ```bash
        python -m venv .venv
        ```
    * (macOS/Linux) Create a Python Virtual Environment:
        ```bash
        python3 -m venv .venv
        ```
    * (Windows) Activate the virtual environment:
        ```bash
        .venv\Scripts\activate
        ```
    * (macOS/Linux) Activate the virtual environment:
        ```bash
        source .venv/bin/activate
        ```
    * Install backend dependencies **(ensure your virtual environment is activated)**:
        ```bash
        pip install -r requirements.txt
        ```
    * *(Note: The virtual environment needs to be activated for backend commands like `uvicorn`)*

4.  **Frontend Setup:**
    * Open a **new** terminal window and navigate to the `frontend` directory:
        ```bash
        cd ../frontend
        ```
    * Ensure Node.js and npm are installed and in your system's PATH. (Check with `node -v` and `npm -v` in a new terminal). If not installed, download from [nodejs.org](https://nodejs.org/).
    * Install frontend dependencies:
        ```bash
        npm install
        ```

## How to Run the Application

1.  **Start the Backend Server:**
    * Open a terminal window and navigate to the `backend` directory.
    * Activate the virtual environment (e.g., `.venv\Scripts\activate` on Windows).
    * Run the server:
        ```bash
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload
        ```
    * Keep this terminal open.

2.  **Start the Frontend Server:**
    * Open a **new** terminal window and navigate to the `frontend` directory.
    * Run the development server:
        ```bash
        npm run dev
        ```
    * Keep this terminal open.

3.  **Access the Application:**
    * Open your web browser and go to `http://localhost:3000`.

## How to Use the Application

* The top section displays the sales representative data fetched from the backend API.  Each representative's deals and region are shown.
* The bottom section ("Ask a Question (AI Endpoint)") allows you to interact with the AI:
    * Type questions about the sales data (e.g., "What are Alice's deals?", "Which rep is in Europe?") and the AI will attempt to answer based on the provided `dummyData.json` context.
    * You can also ask general knowledge questions, and the AI will answer using its base knowledge.

## Challenges and Learnings (Windows Environment Specific)

* Troubleshooting the `npm` or `node` command not being recognized on Windows required repairing the Node.js installation to correctly add it to the system's PATH.
* The `npx tailwindcss init -p` command failed repeatedly, indicating an issue with the executable script creation in `.bin` on Windows. The solution was to manually create `tailwind.config.js` and `postcss.config.js`.
* Accidentally overwriting the `frontend/package.json` file highlighted the importance of careful file management and version control.
* Using `cd /d` is necessary on Windows to change drives in Command Prompt.

## Future Improvements
* Tailwindcss is not properly installed and used.
* Apply more comprehensive Tailwind styling for better visual appeal and responsiveness.
* Implement a more sophisticated data retrieval system for the AI (e.g., using embeddings/vector search).
* Add more robust error handling and user feedback.
* Add backend unit tests.
* Explore deployment strategies.

---
