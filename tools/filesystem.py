from pathlib import Path

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