# AI SQL Agent

A basic AI-powered SQL Agent built using Python, LangChain, Ollama, and PostgreSQL.

The goal of this project is to allow users to interact with a database using natural language instead of writing SQL queries manually.

---

## Current Workflow

```text
User Question
↓
LangChain SQL Agent
↓
Ollama + Gemma4
↓
Schema Inspection
↓
SQL Query Generation
↓
PostgreSQL Execution
↓
Final Response
```

---

## Tech Stack

* Python
* LangChain
* Ollama
* Gemma4
* PostgreSQL
* Docker
* SQLAlchemy

---

## Features Implemented

* Ollama + Gemma4 local setup
* PostgreSQL setup using Docker
* LangChain + Ollama integration
* Python ↔ PostgreSQL connection
* Natural language to SQL workflow
* Schema inspection and table identification
* SQL query generation and execution
* Multi-table JOIN query handling

---

## Sample Queries

```text
Which employee has the highest salary?
```

```text
List all employees with their department names.
```

```text
Show all active projects with employee names.
```

---

## Current Database Tables

* departments
* employees
* projects

---

## How to Run

```bash
source venv/bin/activate
python setup_db.py
python sql_agent_test.py
```

---

## Current Status

This project is currently a working MVP/prototype of an AI SQL Agent that can understand natural language questions, generate SQL queries, execute them on PostgreSQL, and return the final response.
