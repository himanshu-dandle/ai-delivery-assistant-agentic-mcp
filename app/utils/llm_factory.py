import os
import time
from dotenv import load_dotenv

load_dotenv()


def make_response(content: str):
    """
    Creates a simple response object with .content
    so all agents can use response.content consistently.
    """
    return type("Response", (), {"content": content})


def get_llm():
    """
    Select LLM provider from .env.

    Supported values:
    - openai
    - gemini
    - groq
    - mock
    """
    provider = os.getenv("LLM_PROVIDER", "mock").lower().strip()

    if provider == "openai":
        return get_openai_llm()

    if provider == "gemini":
        return get_gemini_llm()

    if provider == "groq":
        return get_groq_llm()

    return get_mock_llm()


def get_openai_llm():
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip(),
        api_key=os.getenv("OPENAI_API_KEY").strip(),
        temperature=0,
    )


def get_gemini_llm():
    from google import genai

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY").strip())
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

    class GeminiWrapper:
        def invoke(self, prompt: str):
            max_retries = 3

            for attempt in range(max_retries):
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                    )
                    return make_response(response.text)

                except Exception as e:
                    print(f"Gemini error attempt {attempt + 1}/{max_retries}: {e}")
                    time.sleep(2)

            raise Exception("Gemini failed after 3 retries.")

    return GeminiWrapper()


def get_groq_llm():
    from langchain_groq import ChatGroq
    import time

    class GroqWrapper:
        def __init__(self):
            self.model = ChatGroq(
                model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant").strip(),
                api_key=os.getenv("GROQ_API_KEY").strip(),
                temperature=0,
            )

        def invoke(self, prompt):
            max_retries = 3

            for attempt in range(max_retries):
                try:
                    return self.model.invoke(prompt)
                except Exception as e:
                    print(f"Groq error attempt {attempt+1}: {e}")
                    time.sleep(8)

            raise Exception("Groq failed after retries")

    return GroqWrapper()

def get_mock_llm():
    """
    Mock LLM for local development without API calls.

    Important:
    Order matters.
    We check reviewer first, then planner, then architect, then analyst.
    This avoids generic prompt text matching the wrong mock response.
    """

    class MockLLM:
        def invoke(self, prompt: str):
            prompt_lower = prompt.lower()

            # 1. Reviewer response
            if "review comments:" in prompt_lower and "final output:" in prompt_lower:
                content = """
Review Comments:
- Add stronger error handling for external API failures.
- Add test cases for ambiguous and unsupported user queries.
- Add security validation for customer data access.

Final Output:
# AI Delivery Assistant Output

## Requirement Summary
Build an AI assistant for an e-commerce platform to handle order status, return requests, and escalation to human agents.

## Architecture
The solution uses a chat UI, LLM/NLP layer, API integration layer, business logic layer, human escalation workflow, logging, observability, and security controls.

## Implementation Tasks
- Build chat interface.
- Integrate order status API.
- Implement return eligibility workflow.
- Add escalation flow.
- Add authentication and authorization checks.
- Add structured logging.
- Add error handling and fallback responses.
- Add user feedback collection.
- Save final output to markdown file.

## Test Cases
- Test order status lookup.
- Test return eligibility.
- Test escalation.
- Test ambiguous inputs.
- Test unsupported queries.
- Test API failure fallback.
- Test file output creation.

## Review Comments
- Improve API error handling.
- Add security validation.
- Add more edge-case tests.
"""
                return make_response(content)

            # 2. Developer Planner response
            if "implementation tasks:" in prompt_lower and "test cases:" in prompt_lower:
                has_feedback = "reviewer feedback" in prompt_lower and "add stronger" in prompt_lower

                if has_feedback:
                    content = """
Implementation Tasks:
- Build the chat interface for customer interaction.
- Implement order status API integration.
- Implement return eligibility workflow.
- Add escalation workflow for unresolved issues.
- Add authentication and authorization checks.
- Add structured logging for all agent and tool steps.
- Add error handling and fallback responses for external API failures.
- Add user feedback collection for continuous improvement.
- Save final delivery output to markdown file.

Test Cases:
- Verify order status intent is detected correctly.
- Verify return request flow works for eligible and ineligible orders.
- Verify escalation happens when the assistant cannot answer.
- Verify logs are created for each workflow step.
- Verify final output is saved to the expected file path.
- Verify system handles ambiguous user input safely.
- Verify unsupported queries return fallback responses.
- Verify API failure is handled gracefully.
"""
                else:
                    content = """
Implementation Tasks:
- Build the chat interface for customer interaction.
- Implement order status API integration.
- Implement return eligibility workflow.
- Add escalation workflow for unresolved issues.
- Add structured logging for all agent and tool steps.
- Save final delivery output to markdown file.

Test Cases:
- Verify order status intent is detected correctly.
- Verify return request flow works for eligible and ineligible orders.
- Verify escalation happens when the assistant cannot answer.
- Verify logs are created for each workflow step.
- Verify final output is saved to the expected file path.
"""
                return make_response(content)

            # 3. Solution Architect response
            if "solution architect" in prompt_lower or "overall solution approach" in prompt_lower:
                content = """
# High-Level Architecture Plan

## 1. Overall Solution Approach
Build a conversational AI assistant that understands customer questions, retrieves order or return information through APIs, and escalates unresolved cases to human agents.

## 2. Main Components
- Chat UI for customer interaction.
- NLP/LLM layer for intent understanding and response generation.
- API integration layer for order and return systems.
- Business logic layer for escalation decisions.
- Human agent dashboard for escalated issues.
- Logging and observability layer.
- Security and data privacy layer.

## 3. Agent Workflow Design
1. Customer asks a question.
2. Assistant identifies intent.
3. Assistant calls relevant API or knowledge source.
4. Assistant responds or escalates.
5. Human agent receives full context when escalation happens.

## 4. Tool Usage Points
- Order status lookup tool.
- Return eligibility checker.
- Escalation ticket creation tool.
- File/document output tool.

## 5. Human-in-the-Loop Checkpoint
Human approval is required before proceeding from architecture to implementation planning.

## 6. Observability/Logging Approach
Log each agent step, important state changes, API/tool calls, errors, and final output path.
"""
                return make_response(content)

            # 4. Requirement Analyst response
            if "senior requirement analyst" in prompt_lower:
                content = """
Requirement Summary:
Build an AI assistant for an e-commerce platform to handle order status, return requests, and escalation to human agents.

Assumptions:
- The assistant will integrate with an existing order management system.
- Customers will use a web or mobile chat interface.
- The MVP will support English language interactions.

Constraints:
- The system must protect customer data.
- The system should support human escalation.
- The system should include logging and basic observability.
"""
                return make_response(content)

            return make_response("Mock response generated.")

    return MockLLM()