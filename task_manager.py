import time
import csv
import os
import logging

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging (if not already configured elsewhere)
logging.basicConfig(
    filename="logs/agent.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Task:
    def __init__(self, name, func, args, metadata=None):
        self.name = name
        self.func = func
        self.args = args
        self.status = "Pending"  # Options: Pending, Running, Completed, Failed
        self.attempts = 0
        self.output = ""
        self.metadata = metadata or {}  # For storing additional info (e.g., target)

class TaskManager:
    def __init__(self, max_retries=3):
        self.tasks = []
        self.max_retries = max_retries

    def add_task(self, task):
        logging.info(f"Adding task: {task.name}")
        self.tasks.append(task)

    def run_tasks(self):
        idx = 0
        while idx < len(self.tasks):
            task = self.tasks[idx]
            idx += 1  # increment index here so that new tasks can be appended
            task.attempts = 0
            while task.attempts < self.max_retries:
                try:
                    task.status = "Running"
                    logging.info(f"Running task: {task.name}")
                    print(f"Running task: {task.name}")
                    # Execute task; here we pass alternate parameters if available from metadata
                    alt_args = task.metadata.get("alternate_args")
                    output = task.func(task.args, alternate_args=alt_args)
                    task.output = output
                    task.status = "Completed"
                    logging.info(f"Task {task.name} output:\n{output}")
                    print(f"Task {task.name} output:\n{output}")
                    # Check for dynamic updates: simulate that if output contains "subdomain", add a new task.
                    if "subdomain" in output.lower():
                        self.add_task(Task(
                            name=f"Subdomain Scan for {task.metadata.get('target', 'unknown')}",
                            func=task.func,  # For demonstration, reusing same function
                            args=task.args + ["-deep"],
                            metadata=task.metadata
                        ))
                    break
                except Exception as e:
                    task.attempts += 1
                    logging.error(f"Task {task.name} failed (attempt {task.attempts}): {e}")
                    print(f"Task {task.name} failed (attempt {task.attempts}): {e}")
                    time.sleep(2)
                    if task.attempts >= self.max_retries:
                        task.status = "Failed"
                        logging.error(f"Task {task.name} failed after {self.max_retries} attempts.")
                        print(f"Task {task.name} failed after {self.max_retries} attempts.")
        # After executing all tasks, write task statuses to CSV
        self.write_task_statuses()

    def write_task_statuses(self, filename="logs/task_statuses.csv"):
        with open(filename, "w", newline="") as csvfile:
            fieldnames = ["name", "status", "attempts"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for task in self.tasks:
                writer.writerow({
                    "name": task.name,
                    "status": task.status,
                    "attempts": task.attempts
                })
        logging.info("Task statuses written to " + filename)
        print("Task statuses written to " + filename)

if __name__ == "__main__":
    # Example usage with a dummy task that triggers dynamic update.
    def dummy_func(args, alternate_args=None):
        # Simulate output; if "-trigger" in args, output contains "subdomain"
        if "-trigger" in args:
            return "Scan complete. Found subdomain: sub.example.com"
        return "Dummy output: " + " ".join(args)
    
    tm = TaskManager(max_retries=2)
    tm.add_task(Task("Initial Dummy Task", dummy_func, ["-trigger", "test"], metadata={"target": "example.com"}))
    tm.run_tasks()
