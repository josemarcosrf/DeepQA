## Dockerfile to build DeepQ&A container image for REST server
FROM python:3.6-slim

SHELL ["/bin/bash", "-c"]

## General Dependencies
RUN apt-get update -qq \
    && apt-get install -y \
    --no-install-recommends \
    build-essential \
    git-core \
    unzip \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Project specific python dependencies
COPY requirements.txt .
RUN  pip3 install -r requirements.txt --no-cache-dir
RUN [ "python3", "-c", "import nltk; nltk.download('punkt')" ]

COPY ./ /root/DeepQA

VOLUME ["/root/DeepQA/save", "/root/DeepQA/data"]

EXPOSE 9002

# Launch the server
WORKDIR /root/DeepQA/
CMD python3 server.py --port 9002
