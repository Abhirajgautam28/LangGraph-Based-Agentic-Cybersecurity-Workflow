# CybersecurityAgent

A LangGraph-based agentic cybersecurity pipeline that dynamically executes security scans using Dockerized security tools (e.g., Gobuster, FFUF, SQLMap) while enforcing user-defined target scopes. The agent autonomously parses high-level security instructions, manages a dynamic task list with retry logic, logs all activities, and generates a final audit report.

## Table of Contents
- [CybersecurityAgent](#cybersecurityagent)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Project Structure](#project-structure)
  - [Environment Setup](#environment-setup)
    - [1. Install Dependencies](#1-install-dependencies)
    - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
  - [Installation](#installation)
    - [Clone the Repository](#clone-the-repository)
    - [Install Python Dependencies](#install-python-dependencies)
    - [Build Docker Images](#build-docker-images)
  - [Configuration](#configuration)
  - [Running the Application](#running-the-application)
    - [Execution Flow](#execution-flow)
  - [Testing \& Verification](#testing--verification)
    - [Check Logs](#check-logs)
  - [Optional Visual Interface](#optional-visual-interface)
    - [Dashboard Features](#dashboard-features)
  - [Future Enhancements](#future-enhancements)

## Overview

This project simulates a real-world security audit assistant by:
- **Breaking down** high-level security instructions into an ordered list of tasks.
- **Executing** each task sequentially, handling failures with retries and alternate configurations.
- **Enforcing** target scope restrictions so that only approved domains/IP ranges are scanned.
- **Integrating** dynamic updates by parsing intermediate scan outputs.
- **Logging** every action and generating a final audit report summarizing the performed steps and any issues discovered.

## Features

- **Dynamic Task List** - Simulated integration with LangChain/LangGraph to convert high-level instructions into granular tasks.
- **Robust Failure Detection** - Implements multiple retries with alternate parameters for failed tasks.
- **Scope Enforcement** - Checks each scan target against a user-defined scope before executing the task.
- **Docker Integration** - Runs security tools via Docker containers, avoiding native installation on Windows.
- **Detailed Logging** - Writes execution logs to `logs/agent.log` and task statuses to `logs/task_statuses.csv`.
- **Final Audit Report** - Generates a comprehensive report at `logs/audit_report.txt`.
- **Real-Time Dashboard (Optional)** - A Streamlit app displays task statuses, logs, and the final audit report.

## Project Structure

```
CybersecurityAgent/
├── .venv/                 # Virtual environment (created locally)
├── config.py              # Loads configuration from .env file
├── scope_enforcer.py      # Enforces target scope restrictions
├── tool_executor.py       # Executes Docker-based security tools with logging and retry logic
├── task_manager.py        # Manages tasks: ordering, execution, dynamic updates, and CSV logging
├── agent.py               # High-level agent logic that integrates parsing, scope enforcement, and reporting
├── main.py                # Entry point: loads config, gets user instruction, and runs the agent
├── streamlit_app.py       # (Optional) Dashboard for visualizing task statuses and logs in real time
├── tests/
│   └── test_agent.py      # Unit tests for scope enforcement, dynamic task parsing, and filtering
├── logs/                  # Folder where logs, task statuses, and audit report are stored
├── requirements.txt       # Python dependencies
└── README.md              # Project overview and instructions (this file)
```

## Environment Setup

### 1. Install Dependencies
- **Python 3.11** - Download and install from [python.org](https://www.python.org/downloads/).
- **Docker Desktop for Windows** - Install Docker Desktop from [Docker Desktop](https://www.docker.com/products/docker-desktop) and ensure Docker is running with WSL2 backend.

### 2. Create a Virtual Environment
```sh
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
.\.venv\Scripts\Activate   # On Windows
```

## Installation

### Clone the Repository
```sh
git clone https://github.com/Abhirajgautam28/LangGraph-Based-Agentic-Cybersecurity-Workflow.git
cd CybersecurityAgent
```

### Install Python Dependencies
```sh
pip install -r requirements.txt
```

### Build Docker Images
```sh
docker build -t my-gobuster -f Dockerfile.gobuster .
docker build -t my-ffuf -f Dockerfile.ffuf .
docker build -t my-sqlmap -f Dockerfile.sqlmap .
```

## Configuration
Create a `.env` file in the project root with content similar to:
```
# .env file sample
TARGET_SCOPE=google.com,.example.com,192.168.1.0/24
MAX_RETRIES=3
LOG_LEVEL=INFO
```

## Running the Application
Run the agent:
```sh
python main.py
```
When prompted, enter a high-level security instruction, e.g.:
```
Scan google.com for open ports and discover directories.
```

### Execution Flow
- The agent converts the instruction into tasks.
- Tasks are verified against the target scope.
- Tasks execute with retry logic and alternate parameters if needed.
- Logs are recorded.
- A final audit report is generated at `logs/audit_report.txt`.

## Testing & Verification
Run unit tests using pytest:
```sh
pytest tests/
```

### Check Logs
- **Logs:** `logs/agent.log`
- **Task Statuses:** `logs/task_statuses.csv`
- **Audit Report:** `logs/audit_report.txt`

## Optional Visual Interface
A Streamlit dashboard is available for visualization:
```sh
streamlit run streamlit_app.py
```

### Dashboard Features
- Displays the dynamic task list with statuses (Pending, Running, Completed, Failed).
- Shows real-time log outputs from `logs/agent.log`.
- Presents the final audit report from `logs/audit_report.txt`.

## Future Enhancements
- **Dynamic Task Updates:** Integrate real LangChain/LangGraph APIs for task automation.
- **Robust Failure Recovery:** Auto-adjust parameters (e.g., port ranges, wordlists) upon failures.
- **Enhanced Scope Enforcement:** Strict validation for out-of-scope scans.
- **Extended Reporting:** Include detected vulnerabilities and scope violation summaries.
- **Additional Unit Tests:** Expand coverage for dynamic behaviors and failures.
