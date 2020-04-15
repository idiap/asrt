import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='asrt',
    version='1.0',
    author="Alexandre Nanchen",
    author_email="alexandre.nanchen@idiap.ch",
    description="Text unformatting and classification library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idiap/asrt",
    keywords="Text, unformatting, processing",
    license="BSD 3-Clause License",
    packages=["asrt"],
    zip_safe = False,
    include_package_data = True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD-3-Clause",
        "Operating System :: Linux",
    ],
    install_requires =[
        "nltk",
        "roman",
        "num2words",
        "unicodecsv",
    ],
    scripts = [
        "asrt/data-preparation/bash/run_data_preparation.sh",
        "asrt/data-preparation/python/run_apply_regex.py",
        "asrt/data-preparation/python/run_data_preparation_individual_files.py",
        "asrt/data-preparation/python/run_data_preparation.py",
        "asrt/data-preparation/python/run_data_preparation_task.py",
        "asrt/data-preparation/python/run_test_regex.py",
        "asrt/examples/bash/run_data_preparation.sh",
        "asrt/examples/bash/run_data_preparation_task.sh",
        "asrt/config/AsrtConfig.sh",
        "asrt/setenv",
    ],
    package_data={'asrt': ['examples/resources/*',
                           'data-preparation/python/2012_05_Sessiondemai2012.pdf',
                           'data-preparation/python/2015.03_Sessiondemars2015.pdf',
                           'data-preparation/python/regex_mediaparl.csv',
                           'common/unit_test/resources/*',
                           'common/unit_test/resources/target-folder-1/*',
                           'common/unit_test/resources/target-folder-2/*',
                           'common/unit_test/resources/target-folder-err-1/*',
                           'common/unit_test/resources/target-folder-err-2/*',
                           'common/unit_test/resources/target-folder-err/*']}
)
