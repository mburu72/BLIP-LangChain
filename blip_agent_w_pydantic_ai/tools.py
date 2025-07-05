from pydantic_ai import RunContext
from docs_processing.docsops import split_embed, load_docs

documents = load_docs('compliance_docs/Kenya/')

async def a_retrieve(cxt: RunContext[str]):
    """Get context from available documents using similarity search."""
    v_store = split_embed(documents)
    docs = v_store.similarity_search(cxt.prompt)
    return [d.page_content for d in docs]
