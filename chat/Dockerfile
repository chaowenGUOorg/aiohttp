FROM python
RUN ["python", "-m", "venv", "--copies", "/usr/local/src/venv"]
COPY server.py /usr/local/src/venv
WORKDIR /usr/local/src/venv
RUN ["./bin/pip", "install", "aiohttp", "uvloop", "aiokafka"]
RUN ["./bin/python", "-m", "compileall", "-lb", "."]
RUN ["rm", "-rf", "*.py"]

FROM scratch
ARG VERSION
WORKDIR /usr/local/src/venv
COPY --from=0 /usr/local/src/venv .
COPY --from=python:slim /usr/local/lib/libpython$VERSION.so.1.0 /usr/lib/x86_64-linux-gnu/
COPY --from=python:slim /usr/local/lib/python$VERSION /usr/local/lib/python$VERSION/
COPY --from=python:slim /lib/x86_64-linux-gnu /lib/x86_64-linux-gnu/
COPY --from=python:slim /usr/lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu/
COPY --from=python:slim /lib64 /lib64/
ENTRYPOINT ["./bin/python", "server.pyc"]
