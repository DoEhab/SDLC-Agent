import json
from pathlib import Path
from urllib import response

from llm import ask_llm
from tools.filesystem import write_file, clone_repo


def generate_code(repo_url, task, analysis):

    # 1. Clone GitHub repository locally
    local_repo_path = clone_repo(repo_url)

    print(f"Cloned repository to: {local_repo_path}")

    # 2. Ask LLM to generate the modified files
    print("1. Passing code analysis to LLM...")

    prompt = f"""
You are a software engineering agent.

This is the code: 
{repo_url}
The task:
{task}


Based on this code analysis:
{analysis}

Generate the required code changes.
Before returning the changes, verify mentally that:
- all referenced classes and fields exist
- imports are correct
- method names match the existing interfaces
- the generated code is consistent across files
- no undefined variables or dependencies are introduced
- existing functionality is preserved
You may modify only the files necessary for the requested task.
Do not modify unrelated files.
Return ONLY valid JSON.

The JSON must be an object where:
- each key is a repository-relative file path
- each value is the complete modified file content

Example:

{{
    "src/main/java/example/Payment.java": "full file content",
    "src/main/java/example/PaymentService.java": "full file content"
}}
"""


    print("2. Sending request to Cohere...")

    response = ask_llm(prompt).strip()

    if response.startswith("```"):
        response = response.split("\n", 1)[1]
        response = response.rsplit("```", 1)[0]

    # 3. Convert LLM JSON response to Python dictionary
    changes = json.loads(response)

    print("3. Writing generated files...")

    # 4. Write each file inside the cloned repository
    for file_path, content in changes.items():

        full_path = Path(local_repo_path) / file_path

        print(f"Writing: {full_path}")

        write_file(full_path, content)

    print("4. Code changes written successfully.")