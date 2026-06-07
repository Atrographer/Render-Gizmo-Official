from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from db_loader import load_dictionary
from my_engine import GizmoEngine

app = FastAPI(title="GIZMO - CLOCK THEE PRECISION AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load database and engine
db_data = load_dictionary()
gizmo = GizmoEngine(db_data)

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "").strip()
    
    if not message:
        return JSONResponse({"response": "Please enter a word to look up."})
    
    response_text = gizmo.lookup(message)
    return {"response": response_text}


if __name__ == "__main__":
    print("=== GIZMO - CLOCK THEE PRECISION AI STARTED ===")
    print("FastAPI server running at http://127.0.0.1:5000/api/chat")
    uvicorn.run(app, host="0.0.0.0", port=5000)
