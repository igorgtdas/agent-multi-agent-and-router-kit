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
    def __init__(self, use_memory: bool = False, window_size: int = 3):
        self._use_memory = use_memory
        self._window_size = window_size
        self._history: dict[str, list[dict[str, str]]] = {}
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
            {"messages": self._build_messages(thread_id, question)},
            config=config,
            context=Context(user_id=thread_id),
        )
        structured = response["structured_response"]
        self._record_history(thread_id, question, structured)
        log_event(
            "agent_response",
            {"thread_id": thread_id, "response": to_jsonable(structured)},
            CONFIG,
        )
        return structured

    def _build_messages(self, thread_id: str, question: str) -> list[dict[str, str]]:
        user_message = {"role": "user", "content": question}
        if not self._use_memory or self._window_size <= 0:
            return [user_message]
        history = self._history.get(thread_id, [])
        max_messages = self._window_size * 2
        return history[-max_messages:] + [user_message]

    def _record_history(self, thread_id: str, question: str, structured) -> None:
        if not self._use_memory or self._window_size <= 0:
            return
        assistant_text = getattr(structured, "agent_response", str(structured))
        new_entries = [
            {"role": "user", "content": question},
            {"role": "assistant", "content": assistant_text},
        ]
        history = self._history.get(thread_id, [])
        max_messages = self._window_size * 2
        self._history[thread_id] = (history + new_entries)[-max_messages:]
