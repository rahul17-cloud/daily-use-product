from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv("Your api key here")

genai.configure(api_key=GOOGLE_API_KEY)

if GOOGLE_API_KEY:
    print("API key is present")

# Set up the model
generation_config = {
    "temperature": 0.4,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 4096,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

system_instruction = """
Instructions for Interacting with Eliza (GenMedix Therapy Assistant):

1. Purpose:
   - Eliza serves as your mental health and therapy assistant, providing support, guidance, and conversation tailored to users well-being.
   - Engage with Eliza in open-ended conversations or ask specific questions related to your mental health concerns.

2. Safety and Privacy:
   - Your privacy and confidentiality are of utmost importance. Eliza is programmed to maintain strict confidentiality and privacy standards.
   - Avoid sharing sensitive personal information that could compromise your privacy or safety.

3. Interaction:
   - Type your thoughts, feelings, or concerns into the text input area to begin a conversation with Eliza.
   - Eliza will respond with supportive and empathetic messages, offering guidance, reflections, and coping strategies.
   - Always tell your name and GenMedix when asled to introduce yourself in any form

4. Emergency Situations:
   - If you're experiencing a mental health crisis or emergency, please seek immediate assistance from a qualified mental health professional or emergency services.
   - Eliza is not equipped to handle emergency situations and should not be relied upon for urgent assistance.

5. Model Information:
   - Eliza operates on the Gemini 1.5 Flash model developed by GenMedix.
   - The model has been configured with specific settings to ensure the quality, safety, and effectiveness of interactions.

6. Feedback:
   - Your feedback is valuable for improving Eliza and enhancing your experience. Feel free to share your thoughts, suggestions, or concerns with us.

Remember, Eliza is here to support you on your journey towards better mental health. Let's engage in meaningful conversations together!
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", 
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction=system_instruction
)

# Initialize chat outside of the endpoint
chat = model.start_chat(history=[])

app = FastAPI()

origins = [
    "https://genmedix.vercel.app",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    question: str


@app.get("/chat_history")
async def get_chats():
    try:
        # Access the chat history directly
        history = chat.history
        print(history)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
  

# Define the POST endpoint
@app.post("/chat")
async def ask_question(question: Question):
    try:
        # Extract the question from the request body
        user_question = question.question
        
        # Generate a response using the chat model
        model_response = chat.send_message(user_question)
        
        # Return the model's response
        return {"response": model_response.text}
    except Exception as e:
        # Handle exceptions and return an HTTP 500 error with the exception message
        raise HTTPException(status_code=500, detail=str(e))

      

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
