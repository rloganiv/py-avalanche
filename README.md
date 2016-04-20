py-avalanche
============

Summary: A Python implementation of the Bank Avalanche Model.

Installing py-avalanche
=======================

## System setup
You'll need to install the header files for Python 2.7. On
Ubuntu you should be able to install like this:

```bash
sudo apt-get -y install python2.7-dev
```

## Python setup
<<<<<<< HEAD
The preprocessing script is written in Python 2.7; its dependencies are in the
file `requirements.txt`.
=======
The project dependencies are in the file `requirements.txt`.
>>>>>>> Updated README.md file
You can install these dependencies in a virtual environment like this:

```bash
virtualenv .env                  # Create the virtual environment
source .env/bin/activate         # Activate the virtual environment
pip install -r requirements.txt  # Install Python dependencies
# Work for a while ...
deactivate                       # Exit the virtual environment
```
