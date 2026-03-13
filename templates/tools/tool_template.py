import json

from langchain.tools import tool, ToolRuntime

from core.logger import log_event
from core.settings import load_config
from tools.context import Context

CONFIG = load_config()
TOOL_NAME = "tool_template"


def _error_output(message: str) -> str:
    return json.dumps({"success": False, "message": message}, ensure_ascii=False)


def _fail(runtime: ToolRuntime[Context] | None, message: str) -> str:
    if runtime is not None:
        runtime.context.tool_failures.setdefault(TOOL_NAME, message)
    output = _error_output(message)
    log_event(
        "tool_result",
        {"tool": TOOL_NAME, "output": output},
        CONFIG,
    )
    return output


@tool
def tool_template(runtime: ToolRuntime[Context], param: str) -> str:
    """Describe what this tool does."""
    previous_error = runtime.context.tool_failures.get(TOOL_NAME)
    if previous_error:
        output = _error_output(previous_error)
        log_event(
            "tool_blocked",
            {"tool": TOOL_NAME, "reason": previous_error},
            CONFIG,
        )
        return output
    log_event(
        "tool_call",
        {"tool": TOOL_NAME, "input": {"param": param}},
        CONFIG,
    )
    try:
        output = f"OK: {param} (user_id={runtime.context.user_id})"
        log_event(
            "tool_result",
            {"tool": TOOL_NAME, "output": output},
            CONFIG,
        )
        return output
    except Exception:
        return _fail(runtime, "erro de conexão com API")
