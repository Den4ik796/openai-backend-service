from sqlalchemy.orm import Session as DBSession
from openai import OpenAI
from fastapi import HTTPException
import database
from config import settings, PRICING

def calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    rates = PRICING.get(model)
    if not rates:
        return 0.0
    return (prompt_tokens * rates["prompt_price_per_token"]) + (completion_tokens * rates["completion_price_per_token"])

def process_chat_message(session_id: int, user_content: str, db: DBSession):
    if not settings.openai_api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key is missing. Check your .env file.")
        
    client = OpenAI(api_key=settings.openai_api_key)
    
    db_session = db.query(database.ChatSession).filter(database.ChatSession.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    user_msg = database.Message(session_id=session_id, role="user", content=user_content)
    db.add(user_msg)
    db.commit()

    history = db.query(database.Message).filter(database.Message.session_id == session_id).order_by(database.Message.id).all()
    
    messages_for_openai = [{"role": "system", "content": "You are a helpful assistant."}]
    for msg in history:
        messages_for_openai.append({"role": msg.role, "content": msg.content})

    try:
        response = client.chat.completions.create(
            model=settings.model_name,
            messages=messages_for_openai
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"OpenAI API Error: {str(e)}")

    assistant_content = response.choices[0].message.content
    usage = response.usage

    prompt_t = usage.prompt_tokens
    comp_t = usage.completion_tokens
    cost = calculate_cost(settings.model_name, prompt_t, comp_t)

    assistant_msg = database.Message(
        session_id=session_id, 
        role="assistant", 
        content=assistant_content,
        prompt_tokens=prompt_t,
        completion_tokens=comp_t
    )
    db.add(assistant_msg)

    db_session.total_tokens += (prompt_t + comp_t)
    db_session.total_cost += cost
    db.commit()

    return assistant_msg
