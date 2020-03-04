import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    version='1.0',
    author="Alexandre Nanchen",
    author_email="alexandre.nanchen@idiap.ch",
    description="Text unformatting and classification library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idiap/asrt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD-3-Clause",
        "Operating System :: Linux",
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
