from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import process_prompt

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