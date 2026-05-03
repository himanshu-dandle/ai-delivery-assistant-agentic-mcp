from app.graph.state import WorkflowState
from app.prompts.planning_prompts import DEVELOPER_PLANNER_PROMPT
from app.utils.llm_factory import get_llm


def developer_planner_agent(state: WorkflowState) -> WorkflowState:
    """
    Generate implementation tasks and test cases from architecture,
    business capability mapping, and reviewer feedback.
    """

    if state["approval_status"] != "approved":
        state["error_message"] = "Architecture not approved. Cannot proceed to planning."
        state["logs"].append("Planner blocked due to missing approval.")
        return state

    llm = get_llm()

    architecture_summary = state["architecture_plan"][:1500]

    capability_map = state.get("tool_results", {}).get("business_capability_map", {})

    capabilities = "\n".join(f"- {c}" for c in capability_map.get("capabilities", [])) or "Not provided"
    data_sources = "\n".join(f"- {d}" for d in capability_map.get("data_sources", [])) or "Not provided"
    integrations = "\n".join(f"- {i}" for i in capability_map.get("integrations", [])) or "Not provided"
    risks = "\n".join(f"- {r}" for r in capability_map.get("risks", [])) or "Not provided"

    review_feedback = ""
    if state["review_comments"]:
        review_feedback = "\n".join(f"- {comment}" for comment in state["review_comments"])

    prompt = f"""
{DEVELOPER_PLANNER_PROMPT}

Requirement Summary:
{state["requirement_summary"]}

Architecture Plan (Summarized):
{architecture_summary}

Business Capabilities:
{capabilities}

Data Sources:
{data_sources}

Integrations:
{integrations}

Risks:
{risks}

Reviewer Feedback:
{review_feedback}

IMPORTANT INSTRUCTIONS:
- You MUST create implementation tasks aligned to integrations such as OMS, CRM, notification systems, or other mapped integrations.
- You MUST create tasks for each data source, including ingestion, validation, access control, and data quality checks.
- You MUST include tasks for risk mitigation, including security, latency, failure handling, escalation delay, and privacy controls.
- You MUST create detailed test cases for API failures, ambiguous inputs, data consistency, escalation scenarios, security validation, and performance.
- Do NOT generate generic tasks.
- Make tasks implementation-ready and system-specific.
- Use clear naming:
  External systems (OMS, CRM, Notification System)
  Internal services (Order Service, Support Service, Notification Service)
- Avoid duplicate naming like OMS ↔ OMS Service.
"""

    response = llm.invoke(prompt)
    response_text = response.content

    tasks = []
    test_cases = []
    current_section = None

    for line in response_text.splitlines():
        clean_line = line.strip()

        if not clean_line:
            continue

        if clean_line.startswith("Implementation Tasks:"):
            current_section = "tasks"
            continue

        if clean_line.startswith("Test Cases:"):
            current_section = "tests"
            continue

        if current_section == "tasks" and clean_line.startswith("-"):
            tasks.append(clean_line[1:].strip())

        elif current_section == "tests" and clean_line.startswith("-"):
            test_cases.append(clean_line[1:].strip())

    state["implementation_tasks"] = tasks
    state["test_cases"] = test_cases
    state["current_agent"] = "developer_planner"
    state["logs"].append("Developer Planner completed successfully.")

    return state