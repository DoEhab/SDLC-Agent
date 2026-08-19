import os

from tools.filesystem import list_files, list_repo_files
from llm import ask_llm

from dotenv import load_dotenv

load_dotenv()

repo = os.getenv('REPO_PATH')

def run_agent(task):
    files = list_repo_files(repo)

    prompt = f"""
        You are a software engineering agent.
        
        Repository files:
        {files}
        
        User task:
        {task}
        
        Analyze the repository and explain which files
        you need to inspect to perform this task.
        """
    response = ask_llm(prompt)
    print(response)

if __name__ == "__main__":
    run_agent(
        "Implement idempotency for POST /payments"
    )