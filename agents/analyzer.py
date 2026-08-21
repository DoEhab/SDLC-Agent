import os

from tools.filesystem import list_files, list_repo_files, read_repo_file
from llm import ask_llm
import re
import json


def analyzer_agent(repo_url, task):
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
    You are a software engineering analysis agent.

    USER TASK:
    {task}

    You previously identified the relevant files.

    Below is the ACTUAL SOURCE CODE retrieved from the repository.
    Each file is explicitly delimited by its repository path.

    {source_code}

    Your job is to analyze the requested task against the actual source code.

    IMPORTANT RULES:
    - Base your analysis ONLY on the source code provided above.
    - Do NOT invent files, classes, methods, APIs, dependencies, or existing behavior that are not present in the provided code.
    - If information required to implement the task is missing from the provided source code, explicitly state that it is unknown.
    - Distinguish between what currently exists and what needs to be added or changed.
    - The file paths in your response must match the paths provided above.

    Analyze the following:

    1. Explain how the current implementation works and how the relevant components interact.
    2. Explain what needs to change to implement the user's task.
    3. Identify which existing files need to be modified.
    4. Identify any new files that need to be created.
    5. For each affected file, describe the specific changes required.
    6. Identify tests that should be added or modified.
    7. Mention any important dependencies, interfaces, or existing code that must be preserved.

    After the analysis, provide a JSON array containing the required code changes.

    The JSON array is the authoritative list of required changes.

    Each item MUST use this format with correct indentation and new lines:

    {{
    "file": "repository/path/to/file",
        "action": "modify",
        "description": "Specific description of the required change"
    }}


    If no code changes are required, return:

    []

    CRITICAL OUTPUT REQUIREMENTS:
    - The JSON array MUST be the final part of your response.
    - Do NOT put anything after the JSON array.
    - Do NOT wrap the JSON array in Markdown code fences.
    - The JSON MUST be valid JSON.
    - Do NOT include comments inside the JSON.
    """
    print("7. Sending source code to Cohere...")

    analysis = ask_llm(analysis_prompt)

    print("8. Analysis:")
    return {
        "analysis": analysis,
        "source_code": source_code
    }


