FROM python:3.11-slim AS base

ENV OPCUA_CONN=0.0.0.0:4840 \
    STRING_MODE=short \
    ADVANCED_CCNFIGS=false \
    GET_HELP=false

WORKDIR /app

# copy server.sh + server.py
COPY server.py server.py
COPY server.sh server.sh

RUN apt-get -y update && apt-get -y upgrade && \
    apt-get -y install python3-pip && \
    pip3 install --upgrade pip opcua==0.98.13 && \
    chmod +x /app/server.sh

FROM base AS deployment
ENTRYPOINT ["/app/server.sh"]

