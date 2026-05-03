import json
from app.tools.code_generation_tool import code_generation_tool


def mcp_handle_request(request: dict) -> dict:
    """
    Simulated MCP server handler
    """

    tool_name = request.get("tool")

    if tool_name == "code_generation":
        result = code_generation_tool(
            request.get("architecture"),
            request.get("tasks"),
        )

        return {
            "status": "success",
            "result": result
        }

    return {
        "status": "error",
        "message": "Unknown tool"
    }