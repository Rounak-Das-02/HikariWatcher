from importlib.metadata import entry_points
from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


requirementPath = 'requirements.txt'
install_requires = [] # Here we'll get: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()


# Setting up

setup(
        name = "hikariWatcher", 
        version = "0.0.1",
        author="Rounak Das",
        author_email="62498036+Rounak-Das-02@users.noreply.github.com",
        description = "Hot-reloading for hikari-lightbulb discord bots",
        long_description=long_description,
        long_description_content_type="text/markdown",
        install_requires=install_requires, # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        licence = "MIT",
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
        ],
        # package_dir={"": "hikariWatcher"},
        packages= ["hikariWatcher"],
        python_requires=">=3.6",
    )