import logging
import subprocess
import os

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="logs/agent.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_docker_tool(image_name, args, alternate_args=None):
    """
    Execute a Docker command using the specified image and arguments.
    If the command fails, try alternate_args if provided.
    """
    command = ["docker", "run", "--rm", "-it", image_name] + args
    try:
        logging.info(f"Executing command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, timeout=300)
        logging.info(f"Command output: {result.stdout}")
        if result.stderr:
            logging.error(f"Command error output: {result.stderr}")
        # Simulate failure if output is empty (for demonstration)
        if not result.stdout.strip() and alternate_args:
            raise Exception("Empty output; trying alternate configuration")
        return result.stdout
    except Exception as e:
        logging.error(f"Error executing command: {e}")
        if alternate_args:
            alt_command = ["docker", "run", "--rm", "-it", image_name] + alternate_args
            logging.info(f"Retrying with alternate configuration: {' '.join(alt_command)}")
            try:
                result = subprocess.run(alt_command, capture_output=True, text=True, timeout=300)
                logging.info(f"Alternate command output: {result.stdout}")
                return result.stdout
            except Exception as ex:
                logging.error(f"Alternate configuration failed: {ex}")
                return f"Error: {ex}"
        return f"Error: {e}"

def run_gobuster(args, alternate_args=None):
    return run_docker_tool("my-gobuster", args, alternate_args)

def run_ffuf(args, alternate_args=None):
    return run_docker_tool("my-ffuf", args, alternate_args)

def run_sqlmap(args, alternate_args=None):
    return run_docker_tool("my-sqlmap", args, alternate_args)

if __name__ == "__main__":
    # Test calls for each tool
    print("Gobuster Help:")
    print(run_gobuster(["-h"]))
    print("FFUF Help:")
    print(run_ffuf(["-h"]))
    print("SQLMap Help:")
    print(run_sqlmap(["-h"]))
