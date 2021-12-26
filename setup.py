import setuptools
import os
import shutil

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Bump-Version-Bot",
    version="0.4.2",
    author="Javid Rzayev",
    author_email="rz.cavid@gmail.com",
    description="Simple Python Bot for Automation Bump Version for Microservice",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Javid907/github-bump-version-bot",
    packages=['bot'],
    scripts=['bin/app.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: *NIX OS's",
    ],
    python_requires='>=3',
)

path = "/etc/version-bump"
try:
    os.mkdir(path)
    print ("Successfully created the directory %s " % path)
except OSError:
    print ("Creation of the directory %s failed" % path)

templatePath = shutil.copy('config/template.yaml', path)
configPath = shutil.copy('config/config.yaml', path)
