from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import Config
from src.agent.tools import tools
from src.agent.prompts import SYSTEM_PROMPT
from src.agent.memory import PostgresConversationMemory
from src.database.connection import get_supabase

_agents: dict[str, any] = {}


def get_agent_for_user(user_id: str):
    if user_id not in _agents:
        supabase = get_supabase()
        memory = PostgresConversationMemory(user_id, supabase, k=10)
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=Config.GEMINI_API_KEY,
            temperature=0.3,
            max_output_tokens=1024,
        )
        agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            memory=memory,
            agent_kwargs={
                "prefix": SYSTEM_PROMPT,
            },
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5,
            max_execution_time=30,
        )
        _agents[user_id] = agent
    return _agents[user_id]
