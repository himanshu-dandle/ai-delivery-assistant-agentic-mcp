# 🚀 AI Delivery Assistant (Agentic AI + MCP)

## 📌 Overview

This project is an **Agentic AI system** that converts business requirements into:

* Architecture design
* Implementation plan
* Test cases
* Starter microservice codebase

It uses **LangGraph-based multi-agent orchestration** and **MCP-style tool integration**.

---

## 🧠 Key Features

### ✅ Multi-Agent Workflow

* Requirement Analyst
* Solution Architect
* Developer Planner
* Reviewer

### ✅ Human-in-the-loop

* Approval step before execution

### ✅ Iterative Refinement

* Reviewer loop improves output

### ✅ MCP-style Tool Integration

* Agent invokes tools via HTTP
* Decoupled tool execution

### ✅ Code Generation

* Generates:

  * FastAPI app
  * Service layer
  * Test files
  * Project structure

---

## ⚙️ Architecture Flow

Requirement → Analyst → Architect → Approval → Planner → Reviewer → MCP Tool → Code Generation

---

## 🧩 Tech Stack

* Python
* LangGraph
* FastAPI
* OpenAI / Groq
* MCP-style tool server

---

## 🚀 How to Run

### 1. Setup

```bash
pip install -r requirements.txt
```

### 2. Start MCP Server

```bash
python -m uvicorn app.tools.mcp_http_server:app --reload
```

### 3. Run Main Workflow

```bash
python -m app.main
```

---

## 📂 Output

* Architecture + Plan → `data/outputs/`
* Generated Code → `data/generated_project/`

---

## 💡 Key Learning

This project demonstrates:

* Agentic AI system design
* Tool orchestration patterns
* MCP-style architecture
* End-to-end AI-driven delivery

---

## 🎯 Future Enhancements

* GitHub MCP integration
* Async tool execution
* Multi-tool orchestration
* Deployment automation

---

## 👤 Author

Himanshu Dandle
