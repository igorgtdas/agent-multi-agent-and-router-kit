from dataclasses import dataclass

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

from core.logger import init_logging, log_event
from core.observability import get_langsmith_callbacks, to_jsonable
from core.settings import load_config
from tools.context import Context

load_dotenv()

CONFIG = load_config()
init_logging(CONFIG)

SYSTEM_PROMPT = """
Papel:
Voce e um agente especialista.

Missao:
Descreva o tipo de ajuda que voce oferece.

Tools:
- tool_exemplo: descreva quando usar.

Regras:
- Liste regras especificas de roteamento/uso de tools.
"""


@dataclass
class ResponseFormat:
    """Response schema for the agent."""

    agent_response: str


class AgentTemplate:
    def __init__(self):
        self._model = init_chat_model(
            CONFIG.llm_model,
            model_provider=CONFIG.llm_provider,
            temperature=CONFIG.llm_temperature,
            timeout=CONFIG.llm_timeout,
            max_tokens=CONFIG.llm_max_tokens,
            top_p=CONFIG.llm_top_p,
            frequency_penalty=CONFIG.llm_frequency_penalty,
            presence_penalty=CONFIG.llm_presence_penalty,
        )
        self._checkpointer = InMemorySaver()
        self._agent = create_agent(
            model=self._model,
            system_prompt=SYSTEM_PROMPT,
            tools=[],
            context_schema=Context,
            response_format=ToolStrategy(ResponseFormat),
            checkpointer=self._checkpointer,
        )

    def run(self, question: str, thread_id: str):
        config = {"configurable": {"thread_id": thread_id}}
        callbacks = get_langsmith_callbacks(CONFIG)
        if callbacks:
            config["callbacks"] = callbacks
        log_event(
            "user_message",
            {"thread_id": thread_id, "content": question},
            CONFIG,
        )
        response = self._agent.invoke(
            {"messages": [{"role": "user", "content": question}]},
            config=config,
            context=Context(user_id=thread_id),
        )
        structured = response["structured_response"]
        log_event(
            "agent_response",
            {"thread_id": thread_id, "response": to_jsonable(structured)},
            CONFIG,
        )
        return structured
