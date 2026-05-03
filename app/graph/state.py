from typing import TypedDict, List, Dict, Any


class WorkflowState(TypedDict):
    # Original user input
    user_requirement: str

    # Analyst output
    requirement_summary: str
    assumptions: List[str]
    constraints: List[str]

    # Architect output
    architecture_plan: str

    # Human-in-the-loop checkpoint
    approval_status: str
    approval_notes: str

    # Developer planner output
    implementation_tasks: List[str]
    test_cases: List[str]

    # Reviewer output
    review_comments: List[str]
    final_output: str

    # Execution metadata / observability
    current_agent: str
    logs: List[str]

    # Tool / extensibility support
    tool_results: Dict[str, Any]

    # Basic status flags
    error_message: str

    # Loop control
    iteration_count: int