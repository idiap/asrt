# Installation instruction

## Library installation
You can install the library with pip. It will install Python
dependencies and the library itself.

```
pip install .
```

## Additional steps
Perform the following additional steps to complete the installation.

#### Install **pdftotext**
```
# On Mac Osx
pip install poppler

# On Linux
sudo apt-get install pdftotext
```

#### Dowload nltk data and model
- copora : europarl_raw
- model  : punkt

```
# In a bash terminal
NLTK_DATA = '/path to data dir/nltk_data'

mkdir -p $NLTK_DATA
python -m nltk.downloader punkt -d $NLTK_DATA
python -m nltk.downloader europarl_raw -d $NLTK_DATA
```

#### Setup environment variable in you .bashrc

```
# Set to dowloaded location
export NLTK_DATA=/path to the NLTK data folder
```

#### Test the library
```
bash  /library path/examples/bash/run_data_preparation.sh
```

## Docker
To build a docker image of asrt:

```bash
docker build -t asrt .
```

To run `run_data_preparation.py` using docker image, where your test file is
`docker-example/research.txt`:

```bash
docker run -d -v $PWD/docker-example:/usr/local/asrt/data asrt -i data/research.txt -o /usr/local/asrt/data
# Or with the same pdf as above example:
docker run -d -v $PWD/docker-example:/usr/local/asrt/data asrt -i data/Research.pdf -o /usr/local/asrt/data
```

The output will then be in `docker-example/sentences_*.txt`
