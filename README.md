# CybersecurityAgent

A LangGraph-based agentic cybersecurity pipeline that dynamically executes security scans (using tools like nmap, Gobuster, FFUF, and SQLMap via Docker) and enforces a target scope. The agent parses high-level security instructions into a series of tasks, executes them sequentially with retry and failure-handling logic, logs outputs, and produces a final report.

## Table of Contents
- [CybersecurityAgent](#cybersecurityagent)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)

## Overview

This project implements an agentic cybersecurity workflow that:
- Accepts a high-level instruction (e.g., "Scan google.com for open ports and discover directories").
- Breaks down the instruction into a dynamic list of tasks.
- Executes tasks sequentially using Dockerized security tools.
- Enforces a defined target scope to ensure scans stay within allowed domains/IP ranges.
- Logs each action and generates a final report.

The system is built using Python 3.11 with modules for configuration, scope enforcement, task management, and tool execution. Docker containers are used to run Linux-based tools on Windows.

## Installation

### Prerequisites
- **Python 3.11** (download from [python.org](https://www.python.org/downloads/))
- **Docker Desktop for Windows**  
  Install from [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Git** (if needed)

### Setup

1. **Clone/Download the Project:**
   ```bash
   git clone <repository_url>
   cd CybersecurityAgent
