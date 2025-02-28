from config import load_config
from agent import CybersecurityAgent

def main():
    config = load_config()
    instruction = input("Enter high-level security instruction: ")
    agent = CybersecurityAgent(config)
    agent.run(instruction)

if __name__ == "__main__":
    main()
