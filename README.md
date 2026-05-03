# 🚀 AI Delivery Assistant (Agentic AI + MCP)

## 📌 Overview

This project is an **Agentic AI system** that converts business requirements into:

* Architecture design
* Implementation plan
* Test cases
* Starter microservice codebase

It uses **LangGraph-based multi-agent orchestration** and **MCP-style tool integration**.

---

## 💼 Real-World Use Case

A business wants to build an AI assistant for customer support in e-commerce.

Instead of manually designing:

* Architecture
* APIs
* Services
* Test cases

This system:

1. Understands requirement
2. Designs architecture
3. Generates implementation plan
4. Validates design
5. Generates starter code

👉 Reduces solution design time from days to minutes.


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


## 🔌 MCP-Style Tool Integration

This system follows a Model Context Protocol (MCP)-style design:

* Agents do not directly call functions
* Instead, they invoke tools via HTTP

Example:

Agent → POST /mcp → Tool Server → Code Generation

This enables:

* Decoupled architecture
* External tool integration
* Future extensibility (GitHub, DB, APIs)

## 🎯 Why This Project Matters

Most AI projects stop at chatbots or RAG.

This project demonstrates:

* End-to-end AI delivery lifecycle
* Agentic orchestration
* System design automation
* Code generation from requirements




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
