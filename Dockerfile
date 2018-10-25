FROM debian:stretch

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    git \
    libpoppler-cpp-dev \
    pkg-config  \
    python2.7 \
    python-dev \
    python-pip \
    python-roman && \
    pip install pdftotext
     

WORKDIR /usr/local

RUN git clone https://github.com/idiap/asrt.git

ADD requirements.txt /usr/local/asrt

WORKDIR /usr/local/asrt
RUN pip install -r requirements.txt

WORKDIR /usr/local/asrt
ENV NLTK_DATA=/usr/local/asrt/nltk_data

RUN mkdir -p NLTK_DATA && \
    python -m nltk.downloader punkt -d $NLTK_DATA && \
    python -m nltk.downloader europarl_raw -d $NLTK_DATA

CMD echo "#==== This is a test of ASRT library in Docker." && \
    ls /usr/local/asrt/examples/resources/* && \
    /usr/local/asrt/examples/bash/run_data_preparation.sh && \
    /usr/local/asrt/examples/bash/run_data_preparation_task.sh