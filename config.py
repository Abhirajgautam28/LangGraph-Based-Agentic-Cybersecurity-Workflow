import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()  # Load variables from .env file
    config = {
        "target_scope": os.getenv("TARGET_SCOPE", "google.com,.example.com,192.168.1.0/24"),
        "max_retries": int(os.getenv("MAX_RETRIES", 3)),
        "log_level": os.getenv("LOG_LEVEL", "INFO")
    }
    return config

if __name__ == "__main__":
    print(load_config())
