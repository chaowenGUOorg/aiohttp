import asyncio, pathlib, os, aiodocker
async def f():
    docker = aiodocker.Docker()
    await docker.images.pull('python', tag='slim')
    container = await docker.containers.create({'Cmd':['python', '-c', 'import platform; print(platform.python_version()[:3])'], 'Image':'python:slim'})
    await container.start()
    pathlib.Path(os.getenv('GITHUB_ENV')).write_text('VERSION=' + ''.join(await container.log(stdout=True)))
    print(pathlib.Path(os.getenv('GITHUB_ENV')).read_text(),flush=True)
    await container.delete(force=True)
    await docker.close()
    
asyncio.run(f())
