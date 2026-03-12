from langchain.tools import tool, ToolRuntime

from core.logger import log_event
from core.settings import load_config
from tools.context import Context

CONFIG = load_config()


@tool
def tool_template(runtime: ToolRuntime[Context], param: str) -> str:
    """Describe what this tool does."""
    log_event(
        "tool_call",
        {"tool": "tool_template", "input": {"param": param}},
        CONFIG,
    )
    output = f"OK: {param} (user_id={runtime.context.user_id})"
    log_event(
        "tool_result",
        {"tool": "tool_template", "output": output},
        CONFIG,
    )
    return output
