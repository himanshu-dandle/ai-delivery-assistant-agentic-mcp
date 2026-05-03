from fastapi import FastAPI
from pydantic import BaseModel
from app.tools.code_generation_tool import code_generation_tool

app = FastAPI()


class MCPRequest(BaseModel):
    tool: str
    architecture: str
    tasks: list


@app.post("/mcp")
def handle_mcp(req: MCPRequest):
    if req.tool == "code_generation":
        result = code_generation_tool(req.architecture, req.tasks)
        return {
            "status": "success",
            "result": result
        }

    return {
        "status": "error",
        "message": "Unknown tool"
    }