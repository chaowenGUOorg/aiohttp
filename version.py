import asyncio, pathlib
process = asyncio.create_subprocess_exec('docker', 'run', 'python:slim', 'python', '-c', 'import platform; print(platform.python_version()[:3])', stdout=asyncio.subprocess.PIPE)
stdout, _ = await process.communicate()
pathlib.Path(os.getenv('GITHUB_ENV')).write_text(stdout.decode())
