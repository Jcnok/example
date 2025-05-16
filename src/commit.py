# src/commit.py
from devops_agent import DevOpsAgent
from dotenv import load_dotenv
import os

def commit_changes():
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))  # Carrega .env na raiz
    agent = DevOpsAgent()
    result = agent.run("Faça commit das alterações atuais seguindo Conventional Commits")
    print(result)

if __name__ == "__main__":
    commit_changes()