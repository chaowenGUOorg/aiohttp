import os, pathlib
print(pathlib.read_text(os.getenv('GITHUB_ENV')))
