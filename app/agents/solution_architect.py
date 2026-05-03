from app.graph.state import WorkflowState
from app.prompts.architecture_prompts import SOLUTION_ARCHITECT_PROMPT
from app.utils.llm_factory import get_llm


def solution_architect_agent(state: WorkflowState) -> WorkflowState:
    """
    Create a high-level architecture plan based on analyst output
    and business capability mapping tool output.
    """

    llm = get_llm()

    feedback = state.get("approval_notes", "")

    capability_map = state.get("tool_results", {}).get("business_capability_map", {})

    capabilities = "\n".join(
        f"- {c}" for c in capability_map.get("capabilities", [])
    ) or "Not provided"

    data_sources = "\n".join(
        f"- {d}" for d in capability_map.get("data_sources", [])
    ) or "Not provided"

    integrations = "\n".join(
        f"- {i}" for i in capability_map.get("integrations", [])
    ) or "Not provided"

    risks = "\n".join(
        f"- {r}" for r in capability_map.get("risks", [])
    ) or "Not provided"

    prompt = f"""
{SOLUTION_ARCHITECT_PROMPT}

User Requirement:
{state["user_requirement"]}

Requirement Summary:
{state["requirement_summary"]}

Assumptions:
{chr(10).join(f"- {item}" for item in state["assumptions"])}

Constraints:
{chr(10).join(f"- {item}" for item in state["constraints"])}

Business Capabilities:
{capabilities}

Data Sources:
{data_sources}

Integrations:
{integrations}

Risks:
{risks}

IMPORTANT INSTRUCTIONS:
- You MUST explicitly use the provided business capabilities in the architecture.
- You MUST explicitly use the provided integrations in the architecture.
- You MUST map each data source to the relevant system component.
- You MUST include risks and mitigation strategies.
- Do NOT give a generic architecture.
- Make the design specific to the business capability mapping.
- Clearly differentiate between external systems and internal services.
- Use naming convention:
  External Systems → OMS, CRM, Notification System
  Internal Services → Order Service, Support Service, Notification Service
- Avoid using same name for both system and service.

Previous Feedback:
{feedback}
"""

    response = llm.invoke(prompt)
    architecture_text = response.content

    state["architecture_plan"] = architecture_text
    state["current_agent"] = "solution_architect"
    state["logs"].append("Solution Architect completed successfully.")

    return state