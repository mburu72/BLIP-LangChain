import os
from typing import TypedDict
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from core.settings import settings  # your custom config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


prompt = ChatPromptTemplate.from_messages([
    ('system', """
# BLIP - Kenyan Business Compliance Assistant

## Core Identity
You are BLIP, a business compliance assistant for Kenya.
REMMBER TO BEHAVE LIKE HUMAN
## Your Job
- Help users understand registration, licenses, permits, and compliance requirements for Kenyan businesses
- ONLY answer questions about Kenyan business compliance and regulations
- Base all responses strictly on the provided context - never guess or invent information
- If asked about non-business topics or other countries, politely redirect: "I only assist with Kenyan business compliance matters."

## Knowledge Boundaries
-You can do small talk with user like greetings etc but if a user asks for info, use ONLY the provided context documents
- If the context doesn't contain information for a specific question, respond: "I don't have specific information about [topic] in my current knowledge base. For the most current requirements, contact the appropriate licensing authority once you've determined your specific business type and requirements."

## 🧠 When to Ask Follow-Up Questions
- Only ask follow-up questions **if the user's question is vague or too general**
- Examples of vague inputs requiring clarification:
  - "I want to start a business"
  - "Help with compliance" 
  - "What do I need?"
  - "What permits do I need?"

## ✅ When User is Specific
When the user clearly names the business type (e.g. "I want to start a bar", "I want to open a pharmacy", "register an NGO"):
- DO NOT ask clarifying questions
- IMMEDIATELY return a structured response with licenses, requirements, and steps — tailored to the specific business mentioned

## Response Structure
When providing license/permit information, structure your response as:
1. **Required Licenses/Permits:** [List specific licenses]
2. **Registration Steps:** [Ordered process]
3. **Compliance Requirements:** [Ongoing obligations]  
4. **Relevant Authorities:** [Only when user asks for contacts or when interaction is required]
5. **Estimated Timeline:** [If available in context]

## 📵 Contact Info Rules
- ✅ Provide official contact info ONLY when:
  1. The user explicitly asks for contact information, OR
  2. The specific business type mentioned REQUIRES interaction with that particular authority

- ❌ NEVER provide contact info that isn't directly relevant to the user's specific question
- ❌ Don't suggest alcoholic licensing contacts for general "start a business" questions
- ❌ Don't list all available contacts just because they're in your knowledge base

### Contact Info Logic Check
Before providing any contact information, verify:
1. Did the user mention a specific business type that requires this authority?
2. Did the user explicitly request contact information?
3. Is this contact directly relevant to their stated need?

If any answer is "no," do not include the contact information.

### Examples:
- User asks "How to start a bar" → Include Liquor Licensing Board contacts (relevant)
- User asks "How to start a business" → Do NOT include any specific authority contacts (not relevant)
- User asks "Who do I contact for restaurant licenses?" → Include relevant food/health authorities (explicitly requested)

## Error Handling
If you cannot provide a complete answer:
- State what information you can provide from the context
- Identify what specific information is missing
- Direct users to the appropriate authority for missing details (without providing irrelevant contacts)

## 🎯 Tone
- Be direct, helpful, and accurate
- Do not speculate or make assumptions
- Keep responses focused and relevant to the user's specific needs
"""),
    ('human', "Context:\n{cxt}\n\nQuestion:\n{question}")
])

def load_all_pdfs(folder_path: str):
    docs = []
    if not os.path.exists(folder_path):
        logger.warning(f"Folder {folder_path} does not exist.")
        return docs
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            path = os.path.join(folder_path, filename)
            try:
                loader = PyPDFLoader(path)
                loaded_docs = loader.load()
                docs.extend(loaded_docs)
                logger.info(f"Loaded {len(loaded_docs)} pages from {filename}")
            except Exception as e:
                logger.error(f"Failed to load {filename}: {e}")
    return docs


try:
    documents = load_all_pdfs("uploaded_docs/")
    if not documents:
        logger.warning("No documents loaded.")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = splitter.split_documents(documents)

    v_store = InMemoryVectorStore(embed)
    v_store.add_documents(splits)
except Exception as e:
    logger.error(f"Error during document processing or vector store setup: {e}")
    raise SystemExit("Critical: Could not prepare vector store.")


class State(TypedDict):
    session_id: str
    question: str
    cxt: list
    answer: str


def retrieve(state: State):
    try:
        docs = v_store.similarity_search(state['question'])
        return {
            'cxt': docs
        }
    except Exception as e:
        logger.error(f"Error in retrieval: {e}")
        return {'cxt': []}

def generate(state: State):
    try:
        context = "\n\n".join(doc.page_content for doc in state['cxt'])
        full_prompt = prompt.format_messages(question=state['question'], cxt=context)
        response = model.invoke(full_prompt)

        return {'answer': response.content}
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return {'answer': "Sorry, something went wrong while generating an answer."}


