import logging
import os.path
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import settings

embed_model = GoogleGenerativeAIEmbeddings(model='models/embedding-001', google_api_key=settings.G_A_K)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_docs(docs_path):
    docs = []
    if not os.path.exists(docs_path):
        logger.warning('Path does not exist')
    for filename in os.listdir(docs_path):
        if filename.endswith('.pdf'):
            path = os.path.join(docs_path, filename)
            try:
                loader = PyPDFLoader(path)
                load = loader.load()
                docs.extend(load)
            except Exception as e:
                print(e)
    split_embed(docs)
    return docs

def split_embed(documents):

    if not documents:
        logger.warning('No docs loaded')
    try:
        doc_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = doc_splitter.split_documents(documents)
        v_store = InMemoryVectorStore(embed_model)
        v_store.add_documents(chunks)
        return v_store
    except Exception as e:
        logger.error(f'Failed to split docs: {e}')
        raise SystemExit("Critical: Could not prepare vector store")


