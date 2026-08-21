import subprocess
from pathlib import Path

import requests


def list_files(directory):
    proj_dir = Path(directory)
    files = []
    if proj_dir.is_dir():
        for file in proj_dir.rglob("*"):
            if file.is_file():
                if ".git" not in file.parts and "target" not in file.parts:
                    files.append(str(file))
        return files

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def write_file(path, generated_code):
    with open(path, "w") as f:
        f.write(generated_code)

def list_repo_files(repo_url):
    parts = repo_url.rstrip("/").split("/")

    owner = parts[-2]
    repo = parts[-1]

    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    response.raise_for_status()

    data = response.json()

    files = []

    for item in data["tree"]:
        if item["type"] == "blob":
            files.append(item["path"])

    return files


def read_repo_file(repo_url, file_path):
    parts = repo_url.rstrip("/").split("/")

    owner = parts[-2]
    repo = parts[-1]

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    return requests.get(data["download_url"], timeout=10).text

def clone_repo(repo_url):
    destination = "./repos/SDLC-Agent"

    subprocess.run(
        ["git", "clone", repo_url, destination],
        check=True
    )

    print("Repository cloned successfully!")