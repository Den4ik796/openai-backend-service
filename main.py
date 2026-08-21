from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
import database, schemas, services
from database import get_db

app = FastAPI(title="OpenAI Chat Backend")

database.init_db()

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def serve_user_ui():
    with open("user_chat.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/admin", response_class=HTMLResponse, include_in_schema=False)
def serve_admin_ui():
    with open("admin.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/sessions", response_model=schemas.SessionResponse)
def create_session(db: Session = Depends(get_db)):
    new_session = database.ChatSession()
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@app.get("/sessions", response_model=List[schemas.SessionResponse])
def get_all_sessions(db: Session = Depends(get_db)):
    return db.query(database.ChatSession).all()

@app.post("/sessions/{session_id}/messages", response_model=schemas.MessageResponse)
def send_message(session_id: int, message: schemas.MessageCreate, db: Session = Depends(get_db)):
    return services.process_chat_message(session_id, message.content, db)

@app.get("/sessions/{session_id}", response_model=schemas.SessionDetailResponse)
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(database.ChatSession).filter(database.ChatSession.id == session_id).first()
    if not session:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Session not found")
    return session
