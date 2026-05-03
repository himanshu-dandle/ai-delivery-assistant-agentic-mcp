

from langgraph.graph import StateGraph, END

from app.graph.state import WorkflowState
from app.agents.requirement_analyst import requirement_analyst_agent
from app.agents.solution_architect import solution_architect_agent
from app.graph.nodes import human_approval_step, save_output_step
from app.agents.developer_planner import developer_planner_agent
from app.agents.reviewer import reviewer_agent
from app.tools.mcp_server import mcp_handle_request


import requests

def code_generation_node(state: WorkflowState) -> WorkflowState:
    """
    Call real MCP HTTP server
    """

    response = requests.post(
        "http://127.0.0.1:8000/mcp",
        json={
            "tool": "code_generation",
            "architecture": state["architecture_plan"],
            "tasks": state["implementation_tasks"]
        }
    )

    data = response.json()

    if data["status"] != "success":
        state["error_message"] = data.get("message", "MCP call failed")
        state["logs"].append("MCP server call failed.")
        return state

    state["tool_results"]["generated_project"] = data["result"]
    state["current_agent"] = "code_generation_tool"
    state["logs"].append("Code generation executed via MCP HTTP server.")

    return state

def route_after_approval(state: WorkflowState) -> str:
    """
    Decide next step after human approval.
    If approved, continue to planner.
    If rejected, go back to solution architect for revision.
    """

    if state["approval_status"] == "approved":
        return "developer_planner"

    return "solution_architect"
import requests

def code_generation_node(state: WorkflowState) -> WorkflowState:
    """
    Call real MCP HTTP server
    """

    response = requests.post(
        "http://127.0.0.1:8000/mcp",
        json={
            "tool": "code_generation",
            "architecture": state["architecture_plan"],
            "tasks": state["implementation_tasks"]
        }
    )

    data = response.json()

    if data["status"] != "success":
        state["error_message"] = data.get("message", "MCP call failed")
        state["logs"].append("MCP server call failed.")
        return state

    state["tool_results"]["generated_project"] = data["result"]
    state["current_agent"] = "code_generation_tool"
    state["logs"].append("Code generation executed via MCP HTTP server.")

    return state

def route_after_review(state: WorkflowState) -> str:
    """
    Decide next step after reviewer.
    If review comments exist and max iteration not reached, go back to planner.
    Otherwise, generate code artifacts.
    """

    if state["iteration_count"] >= 2:
        return "code_generation"

    if state["review_comments"]:
        return "developer_planner"

    return "code_generation"


def build_workflow():
    """
    Build and compile the LangGraph workflow.
    """

    workflow = StateGraph(WorkflowState)

    workflow.add_node("requirement_analyst", requirement_analyst_agent)
    workflow.add_node("solution_architect", solution_architect_agent)
    workflow.add_node("human_approval", human_approval_step)
    workflow.add_node("developer_planner", developer_planner_agent)
    workflow.add_node("reviewer", reviewer_agent)
    workflow.add_node("code_generation", code_generation_node)
    workflow.add_node("save_output", save_output_step)

    workflow.set_entry_point("requirement_analyst")

    workflow.add_edge("requirement_analyst", "solution_architect")
    workflow.add_edge("solution_architect", "human_approval")

    workflow.add_conditional_edges(
        "human_approval",
        route_after_approval,
        {
            "developer_planner": "developer_planner",
            "solution_architect": "solution_architect",
        },
    )

    workflow.add_edge("developer_planner", "reviewer")

    workflow.add_conditional_edges(
        "reviewer",
        route_after_review,
        {
            "developer_planner": "developer_planner",
            "code_generation": "code_generation",
        },
    )

    workflow.add_edge("code_generation", "save_output")
    workflow.add_edge("save_output", END)

    return workflow.compile()