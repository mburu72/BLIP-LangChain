from typing import TypedDict
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, \
    HumanMessagePromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory, RunnableConfig
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from core.settings import settings
import logging
from docs_processing.docsops import load_docs, split_embed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

session_store = {}
vector_s = None
def get_memory(session_id: str):
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]

try:
    model = ChatGoogleGenerativeAI(
        model='gemini-2.0-flash-001',
        google_api_key=settings.G_A_K
    )
    embed = GoogleGenerativeAIEmbeddings(
        model='models/embedding-001',
        google_api_key=settings.G_A_K
    )

except Exception as e:
    logger.error(f"Failed to initialize models: {e}")
    raise SystemExit("Critical: Could not initialize LLM or embeddings.")

def load_prompt(path_to_prompt: str) -> str:
    with open (path_to_prompt, 'r', encoding='utf-8') as f:
        docs = f.read()
        return docs
sys_prompt = load_prompt('prompt.txt')


prompt = ChatPromptTemplate.from_messages([
SystemMessagePromptTemplate.from_template(sys_prompt)
,MessagesPlaceholder(variable_name='history'),
HumanMessagePromptTemplate.from_template("{question}{cxt}")
])
chain = prompt | model
chat_model = RunnableWithMessageHistory(chain, get_memory, input_messages_key='question',
                                        history_messages_key='history')

try:
    documents = load_docs('uploaded_docs/')
    if not documents:
        logger.warning("No documents loaded.")
    ops = split_embed(documents)
    vector_s = ops
except Exception as e:
    logger.error(f"Error during document processing or vector store setup: {e}")
    raise SystemExit("Critical: Could not prepare vector store.")


class State(TypedDict):
    session_id: str
    question: str
    cxt: list
    answer: str
def query_preprocessing(llm: ChatGoogleGenerativeAI, question: str):
    pre_process_prompt = f"""
    You are a helpful assistant that takes a user's query and turns it into a short statement or 
    paragraph so that it can be used in a semantic similarity search on a vector database to return 
    the most similar chunks of content based on the rewritten query. Return 
    the rewritten query. Craft the query to give back the most efficient answers to the user.
    query: {question}
    """
    retrieval_query = llm.invoke(pre_process_prompt)
    return retrieval_query

def retrieve(state: State):
    question = query_preprocessing(llm=model, question=state['question'])
    logger.info(question.content)
    try:
        retriever = vector_s.as_retriever()
        docs = vector_s.similarity_search(question.content)

        return {
            'cxt': docs
        }
    except Exception as e:
        logger.error(f"Error in retrieval: {e}")
        return {'cxt': []}

def generate(state: State):
    try:
        context = "\n\n".join(doc.page_content for doc in state['cxt'])
        response = chat_model.invoke(
            {
                "question": state['question'],
                "cxt": context
            },
            config=RunnableConfig(configurable={'session_id': state['session_id']})
        )
        history = get_memory(state['session_id']).messages
        logger.info(f'OKAY: {response} & {context}')
        for msg in history:
            return {'answer': response.content}
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return {'answer': "Sorry, something went wrong while generating an answer."}


