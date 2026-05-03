from app.graph.state import WorkflowState
from app.prompts.requirement_prompts import REQUIREMENT_ANALYST_PROMPT
from app.utils.llm_factory import get_llm
from app.tools.planning_tools import business_capability_mapper_tool


def requirement_analyst_agent(state: WorkflowState) -> WorkflowState:
    """
    Analyze the user's raw requirement and update workflow state
    with summary, assumptions, and constraints.
    """
    llm = get_llm()

    user_requirement = state["user_requirement"]

    prompt = f"""
{REQUIREMENT_ANALYST_PROMPT}

User Requirement:
{user_requirement}
"""

    response = llm.invoke(prompt)
    response_text = response.content

    summary = ""
    assumptions = []
    constraints = []

    current_section = None

    for line in response_text.splitlines():
        clean_line = line.strip()

        if not clean_line:
            continue

        if clean_line.startswith("Requirement Summary:"):
            current_section = "summary"
            continue
        elif clean_line.startswith("Assumptions:"):
            current_section = "assumptions"
            continue
        elif clean_line.startswith("Constraints:"):
            current_section = "constraints"
            continue

        if current_section == "summary":
            summary += clean_line + " "
        elif current_section == "assumptions" and clean_line.startswith("-"):
            assumptions.append(clean_line[1:].strip())
        elif current_section == "constraints" and clean_line.startswith("-"):
            constraints.append(clean_line[1:].strip())

    state["requirement_summary"] = summary.strip()
    state["assumptions"] = assumptions
    state["constraints"] = constraints
    capability_map = business_capability_mapper_tool(state["user_requirement"])

    state["tool_results"]["business_capability_map"] = capability_map

    state["current_agent"] = "requirement_analyst"
    state["logs"].append("Requirement Analyst completed successfully.")
    state["logs"].append("Business capability mapper tool executed successfully.")


    return state