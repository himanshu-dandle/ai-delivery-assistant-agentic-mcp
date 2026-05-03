from app.graph.state import WorkflowState
from app.graph.workflow import build_workflow


def initialize_state(user_input: str) -> WorkflowState:
    return {
        "user_requirement": user_input,

        "requirement_summary": "",
        "assumptions": [],
        "constraints": [],

        "architecture_plan": "",

        "approval_status": "pending",
        "approval_notes": "",

        "implementation_tasks": [],
        "test_cases": [],

        "review_comments": [],
        "final_output": "",

        "current_agent": "",
        "logs": [],
        "tool_results": {},
        "error_message": "",

        "iteration_count": 0
    }


if __name__ == "__main__":
    user_input = "Build an AI assistant for e-commerce to handle order status, returns, and escalation to human agents."

    state = initialize_state(user_input)

    app = build_workflow()

    final_state = app.invoke(state)

    print("\nFinal Workflow State From LangGraph:\n")
    for key, value in final_state.items():
        print(f"{key}: {value}")