import os

from agents.analyzer import analyzer_agent
from agents.coder import generate_code
from tools.filesystem import clone_repo, list_files, read_file


def run_agent(repo_url, task):
    local_repo_path = clone_repo(repo_url)
    print(f"Cloned repository to: {local_repo_path}")

    result = analyzer_agent(repo_url, task)

    analysis = result["analysis"]
    source_code = result["source_code"]
    changes = generate_code(repo_url, task, source_code, analysis, local_repo_path)

    return changes