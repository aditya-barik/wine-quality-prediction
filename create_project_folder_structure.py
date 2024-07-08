import os

dirs = [
    os.path.join("data", "remote"),
    os.path.join("data", "raw"),
    os.path.join("data", "processed"),
    "notebooks",
    "models",
    "reports",
    "src",
    "tests"
]

for dir in dirs:
    os.makedirs(dir, exist_ok=True)
    with open(os.path.join(dir, ".gitkeep"), "w") as f:
        pass

files = [
    "requirements.txt",
    "dvc.yaml",
    "params.yaml",
    ".gitignore",
    "README.md",
    os.path.join("src", "__init__.py"),
    "tox.ini"
]

for file in files:
    with open(file, "w") as f:
        pass
