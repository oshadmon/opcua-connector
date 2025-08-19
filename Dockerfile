FROM python:3.11-slim AS base

ENV OPCUA_CONN=0.0.0.0:4840 \
    STRING_MODE=short \
    ADVANCED_CCNFIGS=false \
    GET_HELP=false

WORKDIR /app

# copy server.sh + server.py
COPY server_nov.py server.py
COPY server_working.py server_working.py
COPY server.sh server.sh
COPY requirements.txt requirements.txt
COPY base_examples/ base_examples/

RUN apt-get -y update && apt-get -y upgrade && \
    apt-get -y install python3-pip && \
    pip3 install --upgrade pip && \
    pip3 install --upgrade -r ./requirements.txt && \
    chmod +x /app/server.sh

FROM base AS deployment
#ENTRYPOINT ["/bin/bash"]
ENTRYPOINT ["/app/server.sh"]

