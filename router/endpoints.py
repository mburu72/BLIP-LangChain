import logging
import os
import shutil
from fastapi import File, UploadFile, APIRouter, Header
from pydantic import BaseModel

from blip_agent_w_pydantic_ai import agent_service
from blip_agent_w_pydantic_ai.agent_service import run_agent
from docs_processing.docsops import split_embed
from llm_service.llm_service import retrieve, generate, State

router = APIRouter()
UPLOAD_DIR = 'uploaded_docs'
os.makedirs(UPLOAD_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class Query(BaseModel):
    question: str

@router.post('/upload')
async def upload_files(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
        split_embed(file)
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

@router.post('/ask-agent')
async def ask_agent(question: str, session_id: str = Header(None, alias="X-Session-Id")):
    deps: agent_service.Deps = {
        'session_id': session_id,
        'question': question,
        'context': [],
        'answer': ''
    }
    response = await run_agent(question)
    return response.output


