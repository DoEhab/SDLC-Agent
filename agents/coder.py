from urllib import response

from llm import ask_llm
from tools.filesystem import write_file, clone_repo


def generate_code(repo_path, task, analysis):
    clone_repo(repo_path)
    print("Cloned the repository...")
    print("1. Passing code analysis to LLM...")

    prompt = f"""
        You are a software engineering agent.

        Repository URL:
        {repo_path}

        The task:
        {task}
        
        Write the changes in each file based of these analysis:
        {analysis}

        return an dictionary of keys and values.
        The key is file path and value is the full file with generated code
        """

    print("3. Sending request to Cohere...")
    response:dict[str, str]= {}
    response = ask_llm(prompt)

    for key, value in response.items():
        write_file(key, value)

    print("4. Cohere responded")
    print(response)
