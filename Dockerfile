FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    git \
    libpoppler-cpp-dev \
    pkg-config  \
    python3 \
    python3-dev \
    python3-pip \
    python3-roman \
    python3-pip \
    poppler-utils \
    vim


WORKDIR /usr/local

RUN git clone https://github.com/idiap/asrt.git

WORKDIR /usr/local/asrt
RUN python3 -m pip install .

ENV NLTK_DATA=/usr/local/asrt/nltk_data
RUN mkdir -p NLTK_DATA && \
    python3 -m nltk.downloader punkt -d $NLTK_DATA && \
    python3 -m nltk.downloader europarl_raw -d $NLTK_DATA

ENV LANG=1
ENV REGEX=examples/resources/regex.csv

ENTRYPOINT ["asrt/data-preparation/python/run_data_preparation.py", \
    "-l", "0", \
    "-r", "asrt/examples/resources/regex.csv", "-s", "-m"]

# requires -i inputfile -o outputfolder and mounting volume
