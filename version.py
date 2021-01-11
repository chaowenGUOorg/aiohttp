import os, pathlib
print(pathlib.Path(os.getenv('GITHUB_ENV')).read_text())
