import os

from agents.analyzer import analyzer_agent
from agents.coder import generate_code

def run_agent(repo_url, task):
    analysis = analyzer_agent(repo_url,task)
    changes = generate_code(repo_url, task, analysis)

    return changes