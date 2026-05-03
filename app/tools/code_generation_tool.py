import os


def code_generation_tool(architecture: str, tasks: list) -> dict:
    """
    Generate structured project based on architecture + tasks.
    """

    base_path = "data/generated_project"

    os.makedirs(f"{base_path}/app/services", exist_ok=True)
    os.makedirs(f"{base_path}/tests", exist_ok=True)

    # ----------------------------
    # README
    # ----------------------------
    readme_content = f"""# AI Generated Microservices Project

## Architecture
{architecture}

## Implementation Tasks
{chr(10).join(f"- {t}" for t in tasks)}

## Run
pip install -r requirements.txt
uvicorn app.main:app --reload
"""

    # ----------------------------
    # requirements.txt
    # ----------------------------
    requirements = """fastapi
uvicorn
pydantic
pytest
httpx
"""

    # ----------------------------
    # main.py
    # ----------------------------
    main_app = """from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
"""

    # ----------------------------
    # order_service.py
    # ----------------------------
    order_service = """def get_order_status(order_id: str):
    return {"order_id": order_id, "status": "shipped"}
"""

    # ----------------------------
    # support_service.py
    # ----------------------------
    support_service = """def handle_support_query(query: str):
    return {"response": "Support response generated"}
"""

    # ----------------------------
    # notification_service.py
    # ----------------------------
    notification_service = """def send_notification(user_id: str, message: str):
    return {"status": "sent"}
"""

    # ----------------------------
    # test file
    # ----------------------------
    test_file = """from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    """

    # ----------------------------
    # Write files
    # ----------------------------
    with open(f"{base_path}/README.md", "w") as f:
        f.write(readme_content)

    with open(f"{base_path}/requirements.txt", "w") as f:
        f.write(requirements)

    with open(f"{base_path}/app/main.py", "w") as f:
        f.write(main_app)

    with open(f"{base_path}/app/services/order_service.py", "w") as f:
        f.write(order_service)

    with open(f"{base_path}/app/services/support_service.py", "w") as f:
        f.write(support_service)

    with open(f"{base_path}/app/services/notification_service.py", "w") as f:
        f.write(notification_service)

    with open(f"{base_path}/tests/test_health.py", "w") as f:
        f.write(test_file)

    return {"generated_path": base_path}