import os

from tools.filesystem import list_files, list_repo_files, read_repo_file
from llm import ask_llm
import re
import json

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

    Analyze the repository and explain which files need to be inspected
    to complete the task.

    After your explanation, provide the file paths as a JSON array.

    The JSON array MUST be the final part of your response.
    Do not put anything after the JSON array.

    Example:

    [
        "src/main/java/example/PaymentController.java",
        "src/main/java/example/PaymentService.java"
    ]
    """

    print("3. Sending request to Cohere...")
    response = ask_llm(prompt)

    print("4. Cohere responded")
    print(response)

    # 3. Extract the JSON array from the LLM response
    match = re.search(
        r"```json\s*(\[.*?\])\s*```",
        response,
        re.DOTALL
    )

    print("5. Extracting files list...")

    if match:
        files_to_read = json.loads(match.group(1))
    else:
        print("Could not find JSON file list.")
        files_to_read = []

    print(f"Files selected: {len(files_to_read)}")

    # 4. Read the selected files from GitHub
    source_code = {}

    for file in files_to_read:
        print(f"6. Reading file: {file}")

        content = read_repo_file(
            repo_url,
            file
        )

        source_code[file] = content

    # 5. Show what we collected
    print("\n7. Files successfully read:")

    analysis_prompt = f"""
    You are a software engineering agent.

    User task:
    {task}

    You previously identified the relevant files.

    Below is the actual source code from those files:

    {source_code}

    Analyze the actual source code and explain:

    1. How the current implementation works.
    2. What needs to change to implement the requested task.
    3. Which files need to be modified.
    4. What changes should be made in each file.
    5. What tests should be added or modified.

    Do not invent code or files that are not present.
    Base your analysis on the actual source code provided.
    """

    print("7. Sending source code to Cohere...")

    analysis = ask_llm(analysis_prompt)

    print("8. Analysis:")
    print(analysis)

if __name__ == "__main__":
    repo_url = input("Enter GitHub repository URL: ")
    #pass this to the agent
    task = input("What do you want the agent to do? ")

    run_agent(
        repo_url,"Implement idempotency for POST /payments"
    )