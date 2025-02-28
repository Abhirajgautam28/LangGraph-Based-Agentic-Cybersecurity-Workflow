from task_manager import Task, TaskManager
from tool_executor import run_gobuster, run_ffuf, run_sqlmap
from scope_enforcer import is_in_scope
from config import load_config
import os
import logging

def simulated_langchain_parse(instruction):
    """
    Simulate dynamic parsing of the high-level instruction using LangChain/LangGraph.
    In a real integration, you would call the language model API to get a task list.
    Here we split by keywords.
    """
    tasks = []
    instruction_lower = instruction.lower()
    # For demonstration, if the instruction mentions "open ports", add a gobuster scan
    if "open ports" in instruction_lower:
        tasks.append(Task("Gobuster Scan", run_gobuster, ["-h"], metadata={"target": "google.com", "alternate_args": ["dir", "-u", "http://google.com", "-w", "alternative_wordlist.txt"]}))
    # If the instruction mentions "directories", add an FFUF scan
    if "directories" in instruction_lower:
        tasks.append(Task("FFUF Scan", run_ffuf, ["-h"], metadata={"target": "google.com", "alternate_args": ["-u", "http://google.com/FUZZ", "-w", "alternative_dirs.txt"]}))
    # If the instruction mentions "sql", add an SQLMap test
    if "sql" in instruction_lower or "injection" in instruction_lower:
        tasks.append(Task("SQLMap Test", run_sqlmap, ["-h"], metadata={"target": "google.com", "alternate_args": ["--batch"]}))
    return tasks

class CybersecurityAgent:
    def __init__(self, config):
        self.config = config
        self.task_manager = TaskManager(max_retries=config.get("max_retries", 3))
        self.audit_details = []

    def enforce_scope(self, target):
        allowed_scope = self.config.get("target_scope")
        if not is_in_scope(target, allowed_scope):
            logging.warning(f"Target {target} is out-of-scope!")
            return False
        return True

    def parse_instruction(self, instruction):
        # Use simulated LangChain/LangGraph to parse the instruction
        tasks = simulated_langchain_parse(instruction)
        # Enforce scope: remove tasks for out-of-scope targets
        filtered_tasks = []
        for task in tasks:
            target = task.metadata.get("target", "")
            if self.enforce_scope(target):
                filtered_tasks.append(task)
            else:
                logging.warning(f"Task {task.name} blocked due to out-of-scope target: {target}")
        return filtered_tasks

    def run(self, instruction):
        tasks = self.parse_instruction(instruction)
        if not tasks:
            print("No tasks to run. Check your instruction or scope configuration.")
            return
        for task in tasks:
            self.task_manager.add_task(task)
        self.task_manager.run_tasks()
        # Collect final audit details
        self.generate_audit_report()

    def generate_audit_report(self):
        report_lines = []
        report_lines.append("Final Audit Report")
        report_lines.append("===================")
        for task in self.task_manager.tasks:
            line = f"Task: {task.name}, Status: {task.status}, Attempts: {task.attempts}"
            report_lines.append(line)
            self.audit_details.append(line)
        # Write report to logs/audit_report.txt
        audit_file = os.path.join("logs", "audit_report.txt")
        with open(audit_file, "w") as f:
            f.write("\n".join(report_lines))
        logging.info("Audit report generated.")
        print("Audit report generated at", audit_file)

if __name__ == "__main__":
    config = load_config()
    agent = CybersecurityAgent(config)
    instruction = input("Enter high-level security instruction: ")
    agent.run(instruction)
