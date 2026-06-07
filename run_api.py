from fastapi import FastAPI
from pydantic import BaseModel
from my_engine import HomeGrownIndex
from db_loader import load_local_dictionary
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS so your frontend widget can talk to it safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize your custom non-AI index
dictionary_engine = HomeGrownIndex()
load_local_dictionary("dictionary_db.json", dictionary_engine)

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    reply = dictionary_engine.query(request.message)
    return {"response": reply}
