from app.graph.state import WorkflowState
from app.prompts.review_prompts import REVIEWER_PROMPT
from app.utils.llm_factory import get_llm


def reviewer_agent(state: WorkflowState) -> WorkflowState:
    """
    Review the entire solution and generate final output.
    """

    llm = get_llm()

    prompt = f"""
{REVIEWER_PROMPT}

Requirement Summary:
{state["requirement_summary"]}

Architecture Plan:
{state["architecture_plan"]}

Implementation Tasks:
{chr(10).join(f"- {t}" for t in state["implementation_tasks"])}

Test Cases:
{chr(10).join(f"- {t}" for t in state["test_cases"])}
"""

    response = llm.invoke(prompt)
    response_text = response.content

    comments = []
    final_output = ""

    current_section = None

    for line in response_text.splitlines():
        clean_line = line.strip()

        if not clean_line:
            continue

        if clean_line.startswith("Review Comments:"):
            current_section = "comments"
            continue
        elif clean_line.startswith("Final Output:"):
            current_section = "final"
            continue

        if current_section == "comments" and clean_line.startswith("-"):
            comments.append(clean_line[1:].strip())

        elif current_section == "final":
            final_output += clean_line + "\n"

    state["review_comments"] = comments
    state["final_output"] = final_output.strip()
    state["current_agent"] = "reviewer"
    state["logs"].append("Reviewer completed successfully.")
    state["iteration_count"] += 1

    return state