import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from scope_enforcer import is_in_scope
from agent import simulated_langchain_parse, CybersecurityAgent
from config import load_config

def test_is_in_scope():
    allowed = "google.com,.example.com,192.168.1.0/24"
    assert is_in_scope("mail.google.com", allowed)
    assert is_in_scope("test.example.com", allowed)
    assert not is_in_scope("evil.com", allowed)

def test_simulated_parse():
    instruction = "Scan google.com for open ports and discover directories"
    tasks = simulated_langchain_parse(instruction)
    names = [t.name for t in tasks]
    assert "Gobuster Scan" in names
    assert "FFUF Scan" in names

def test_scope_filtering():
    config = load_config()
    agent = CybersecurityAgent(config)
    # Simulate an instruction with an out-of-scope target
    tasks = simulated_langchain_parse("Scan evil.com for open ports")
    # Manually override target to an out-of-scope value
    for task in tasks:
        task.metadata["target"] = "evil.com"
    filtered_tasks = []
    for task in tasks:
        if agent.enforce_scope(task.metadata["target"]):
            filtered_tasks.append(task)
    assert len(filtered_tasks) == 0

if __name__ == "__main__":
    pytest.main()
