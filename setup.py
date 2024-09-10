#! /usr/bin/env python
from setuptools import setup, find_packages

with open('README.rst', 'r') as f:
    long_description = f.read()

setup_params = dict(
    name='fontParts',
    description=("An API for interacting with the parts of fonts "
                 "during the font development process."),
    author='Just van Rossum, Tal Leming, Erik van Blokland, Ben Kiel, others',
    author_email='info@robofab.com',
    maintainer="Just van Rossum, Tal Leming, Erik van Blokland, Ben Kiel",
    maintainer_email="info@robofab.com",
    url='http://github.com/robotools/fontParts',
    license="OpenSource, MIT",
    platforms=["Any"],
    long_description=long_description,
    package_dir={'': 'Lib'},
    packages=find_packages('Lib'),
    include_package_data=True,
    use_scm_version={
         "write_to": 'Lib/fontParts/_version.py',
         "write_to_template": '__version__ = "{version}"',
    },
    setup_requires=['setuptools_scm'],
    install_requires=[
        "FontTools[ufo,lxml,unicode]>=3.32.0",
        "fontMath>=0.4.8",
        "defcon[pens]>=0.6.0",
        "booleanOperations>=0.9.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.8',
    zip_safe=True,
)


if __name__ == "__main__":
    setup(**setup_params)
