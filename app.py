from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel
from agent_core import DreamAgent

app = FastAPI(title="Lucid Echo - Dream Interpreter")
agent = DreamAgent()

class DreamInput(BaseModel):
    text: str

@app.post("/interpret")
def interpret_dream(dream: DreamInput, x_memory_password: str = Header(None)):
    if not x_memory_password:
        raise HTTPException(status_code=400, detail="X-Memory-Password header required")
    try:
        return agent.process_dream(dream.text, x_memory_password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.get("/history")
def get_history(x_memory_password: str = Header(None)):
    if not x_memory_password:
        raise HTTPException(status_code=400, detail="X-Memory-Password header required")
    try:
        return agent.get_dream_history(x_memory_password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
