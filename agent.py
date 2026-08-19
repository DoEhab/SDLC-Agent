import os

from tools.filesystem import list_files, list_repo_files
from llm import ask_llm

from dotenv import load_dotenv

load_dotenv()

repo = os.getenv('REPO_PATH')

def run_agent(repo_url, task):
    print("1. Getting repository files...")
    files = list_repo_files(repo_url)
    print(f"2. Found {len(files)} files")

    prompt = f"""
        You are a software engineering agent.
        
        Repository files:
        {files}
        
        User task:
        {task}
        
        Analyze the repository and explain which files
        you need to inspect to perform this task.
        """
    print("3. Sending request to Cohere...")
    response = ask_llm(prompt)
    print("4. Cohere responded")
    print(response)

if __name__ == "__main__":
    repo_url = input("Enter GitHub repository URL: ")
    #pass this to the agent
    task = input("What do you want the agent to do? ")

    run_agent(
        repo_url,"Implement idempotency for POST /payments"
    )