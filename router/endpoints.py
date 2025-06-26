import os
import shutil
from fastapi import File, UploadFile, APIRouter, Header
from pydantic import BaseModel

from agent_service import State, retrieve, generate

router = APIRouter()
UPLOAD_DIR = 'uploaded_docs'
os.makedirs(UPLOAD_DIR, exist_ok=True)

class Query(BaseModel):
    question: str

@router.post('/upload')
async def upload_files(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
        return {'filename': file.filename, 'status': 'uploaded'}

@router.post("/ask")
async def ask_question(query: Query, session_id: str = Header(None, alias="X-Session-Id")):

    state: State = {
        'session_id': session_id,
        'question': query.question,
        'cxt': [],
        'answer': ''
    }
    state.update(retrieve(state))
    state.update(generate(state))
    return {"answer": state['answer']}


