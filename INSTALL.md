INSTALL
=======
1. Get the libraries:

   `git submodule update --init lib/nltk`

   `git submodule update --init lib/unicodecsv`

2. Install both libraries using the *setup.py* scripts.

   `setup.py install --prefix=/path/to/local/install`

3. Setup nltk data location with environment variable `NLTK_DATA` (see: http://www.nltk.org/data.html)

4. Get nltk_data. In a python terminal:
    - `import nltk`
    - `nltk.download()`
      - copora : europarl_raw
      - model  : punkt
