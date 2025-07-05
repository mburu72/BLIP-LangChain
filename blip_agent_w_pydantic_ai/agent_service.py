import logging
from typing import List, TypedDict
from pydantic.dataclasses import dataclass
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from blip_agent_w_pydantic_ai.tools import a_retrieve
from config.settings import settings
from utils.functions import load_prompt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
model = GeminiModel(model_name='gemini-2.0-flash-001', provider=GoogleGLAProvider(api_key=settings.G_A_K))
prompt = load_prompt('a_prompt.md')

@dataclass
class Deps(TypedDict):
    session_id: str
    question: str
    context: list
    answer: str

#Init the agent
blip_agent = Agent(model = model, deps_type=Deps, retries=2, result_type=str, system_prompt=prompt,
                       tools=[
                        a_retrieve
                       ])
#Run the agent
async def run_agent(query: str):
    try:
        result = await blip_agent.run(query)
        logger.info(result)
        return result
    except Exception as e:
        logger.warning(e)
        raise SystemExit("Something went wrong. Please try again later")




