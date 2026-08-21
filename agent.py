import os

from agents.analyzer import analyzer_agent
from agents.coder import generate_code
from tools.filesystem import clone_repo, list_files, read_file


def run_agent(repo_url, task):

    local_repo_path = clone_repo(repo_url)
    print(f"Cloned repository to: {local_repo_path}")
    file_list = list_files(local_repo_path)
    for file in file_list:
        content = read_file(file)

    analysis = analyzer_agent(repo_url,task)
    changes = generate_code(repo_url, task, analysis)

    return changes