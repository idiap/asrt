INSTALL
=======
This install manual is for Debian based systems.

1. Get the libraries:

   `git submodule update --init lib/nltk`

   `git submodule update --init lib/unicodecsv`

   `git submodule update --init lib/num2words`

2. Install the three libraries using the *setup.py* scripts.

   `setup.py install --prefix=/path/to/local/install`

3. Setup nltk data location with environment variable `NLTK_DATA` (see: http://www.nltk.org/data.html)

4. Get nltk_data. In a python terminal:
    - `import nltk`
    - `nltk.download()`
      - copora : europarl_raw
      - model  : punkt

5. Install the num2words library: https://pypi.python.org/pypi/num2words

6. Install the python-roman library: sudo apt-get install python-roman

7. Build the debian package
    - Change directory into scripts
    - Run the command `debuild` (debian build)

8. Install the library
    - In the scripts directory, run `sudo dpkg -i ../asrt_1.0.0RC1_all.deb`

9. Run the examples to test your installation
    - `/usr/share/asrt/examples/bash/run_data_preparation.sh`
    - `/usr/share/asrt/examples/bash/run_data_preparation_task.sh`
