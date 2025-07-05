from langchain_core.chat_history import InMemoryChatMessageHistory


def load_prompt(path_to_prompt: str) -> str:
    with open (path_to_prompt, 'r', encoding='utf-8') as f:
        docs = f.read()
        return docs

session_store = {}
def get_memory(session_id: str):
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]
