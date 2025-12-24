# Project GenMedix
Team Dev Titans

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Credentials](#credentials)
- [Running_the_Application](#running_the_application)
- [API_Endpoints](#api_endpoints)
- [Contact](#contact)

## Introduction
This project sets up an API using FastAPI to interact with a Generative AI model. The model, configured with specific settings, serves as a mental health assistant named Eliza, capable of engaging in supportive and empathetic conversations.

## Features
- Interactive Chat: Users can ask questions and receive responses from Eliza.
- Configured Model: The AI model is fine-tuned with safety settings and specific parameters to ensure quality and safety.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/yourproject.git
    ```
2. Navigate to the project directory:
    ```bash
    cd projectgenmedix/genmedix_backend
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```


## Credentials
You'll need to get these api keys:
- Gemini API key: https://aistudio.google.com
and add to the code here

GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY" on line 8 of the code

## Running_the_Application
1. Start the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```

2. Access the API:
- Open your browser and go to http://localhost:8000/docs to view the automatically generated API documentation and test the endpoints.


## API_Endpoints
1. Get Chat History:

- GET /chat_history
Retrieves the chat history.

2. Ask a Question:

- POST /chat
Sends a question to Eliza and receives a response.
Request Body:
json
{
  "question": "Your question here"
}


## Contact
For any questions or feedback, please contact us at [samuelajala01@gmail.com].
