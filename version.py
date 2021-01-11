import asyncio, pathlib, os
async def f():
    process = await asyncio.create_subprocess_exec('docker', 'run', 'python:slim', 'python', '-c', 'import platform; print(platform.python_version()[:3])', stdout=asyncio.subprocess.PIPE)
    stdout, _ = await process.communicate()
    pathlib.Path(os.getenv('GITHUB_ENV')).write_text('VERSION=' + stdout.decode())
    
asyncio.run(f())
