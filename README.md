README
======
Authors
-------
Alexandre Nanchen, Christine Marcel

Description
-----------
This is the README for the Automatic Speech Recognition Tools.

This project contains various scripts in order to facilitate the preparation of
ASR related tasks.

Current tasks are:

1. Sentences extraction from pdf files
2. Sentences classification by language
3. Sentences filtering and cleaning

Document sentences can be extracted into single document or batch mode.

For an example on how to extract sentences in batch mode, please have a
look at the `run_data_preparation_task.sh` script located in
`examples/bash` directory.

For an example on how to extract sentences in single document mode,
please have a look at the `run_data_preparation.sh` script located in
`examples/bash` directory.

There is also an API to be used in python code. It is located into the
common package and is called `DataPreparationAPI.py`

# Docker
To build a docker image of asrt:

```bash
docker build -t asrt .
```

To run `run_data_preparation.py` using docker image, where your test file is
`docker-example/research.txt`:

```bash
docker run -d -v $PWD/docker-example:/usr/local/asrt/data asrt -i data/research.txt -o /usr/local/asrt/data
```

The output will then be in `docker-example/sentences_*.txt`
