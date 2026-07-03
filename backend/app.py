# This file is used to connect my frontend to the calculator.py file

from fastapi import FastAPI                         # Web frameowrk to create the backend API
from fastapi.middleware.cors import CORSMiddleware  # Middleware to allow cross-origin requests from the frontend. Basically wont run on the web browser if not present
from pydantic import BaseModel                      # Defines shape of the data
from agent import process_prompt                    # Injects main procssing function

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PromptRequest(BaseModel):
    prompt: str


@app.get("/")
def root():
    return {
        "status": "Backend Running"
    }


@app.post("/calculate")
def calculate(data: PromptRequest):
    # This now passes back the full dictionary payload containing code and calculated text
    response_data = process_prompt(data.prompt)
    return response_data