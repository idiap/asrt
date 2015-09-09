README
======
Author
------
Alexandre Nanchen, Christine Marcel

Description
-----------
This is the README for the Automatic Speech Recognition Tools.

This project contains various scripts in order to facilitate the preparation of
ASR related tasks.

Current tasks ares:

1. Sentences extraction from pdf files
2. Sentences classification by langues
3. Sentences filtering and cleaning

Document sentences can be extracted into single document or batch mode.

For an example on how to extract sentences in batch mode, please have a
look at the `run_data_preparation_task.sh` script located in
`scripts/examples/bash` directory.

For an example on how to extract sentences in single document mode,
please have a look at the `run_data_preparation.sh` script located in
`scripts/examples/bash` directory.

The is also an API to be used in python code. It is located into the
common package and is called `DataPreparationAPI.py`