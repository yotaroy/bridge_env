FROM python:3.8.5-slim-buster

ENV LANG=C.UTF-8

WORKDIR /workspace
RUN chmod -R a+w /workspace

COPY setup.py /workspace
RUN mkdir bridge_env
COPY /bridge_env /workspace/bridge_env

RUN python -m pip install --upgrade pip && \
    python -m pip install .

EXPOSE 2000

ENTRYPOINT ["bridge-server"]