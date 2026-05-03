from app.graph.state import WorkflowState


def human_approval_step(state: WorkflowState) -> WorkflowState:
    """
    Human-in-the-loop checkpoint for architecture approval
    """

    print("\n===== ARCHITECTURE PLAN =====\n")
    print(state["architecture_plan"])

    print("\nDo you approve this architecture? (yes/no): ")
    decision = input().strip().lower()

    if decision == "yes":
        state["approval_status"] = "approved"
        state["approval_notes"] = "Approved by user."
        state["logs"].append("Architecture approved by user.")
    else:
        print("\nEnter reason for rejection: ")
        notes = input()

        state["approval_status"] = "rejected"
        state["approval_notes"] = notes
        state["logs"].append("Architecture rejected by user.")

    state["current_agent"] = "human_approval"

    return state

from app.tools.file_tools import save_final_output_to_file


def save_output_step(state: WorkflowState) -> WorkflowState:
    """
    Save final reviewed output to a markdown file.
    """

    if not state["final_output"]:
        state["error_message"] = "No final output available to save."
        state["logs"].append("Save output skipped because final_output is empty.")
        return state

    saved_path = save_final_output_to_file(state["final_output"])

    state["tool_results"]["saved_output_path"] = saved_path
    state["current_agent"] = "save_output_tool"
    state["logs"].append(f"Final output saved to {saved_path}")

    return state