FROM ubuntu:18.04
MAINTAINER alexandre.nanchen@idiap.ch

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    git \
    locales \
    libpoppler-cpp-dev \
    pkg-config  \
    python3.7 \
    python3.7-dev \
    python3-pip \
    python3-roman \
    poppler-utils \
    vim

RUN locale-gen de_DE.UTF-8 && \
    update-locale LANG=de_DE.UTF-8

ENV LANG de_DE.UTF-8
ENV LANGUAGE de_DE:de
ENV LC_ALL de_DE.UTF-8

WORKDIR /usr/local

RUN git clone https://github.com/idiap/asrt.git

WORKDIR /usr/local/asrt
RUN pip3 install --upgrade pip
RUN python3 -m pip install .

ENV NLTK_DATA=/usr/local/asrt/nltk_data
RUN mkdir -p NLTK_DATA && \
    python3 -m nltk.downloader punkt -d $NLTK_DATA && \
    python3 -m nltk.downloader europarl_raw -d $NLTK_DATA

ENTRYPOINT ["asrt/data-preparation/python/run_data_preparation.py", \
               "-l", "0", \
               "-r", "asrt/examples/resources/regex.csv", \
               "-s", \
               "-m"]

# requires -i inputfile -o outputfolder and mounting volume
