# CJA License Server

License server used to validate client licenses of CJA product

### Prerequisites

We use python 3 in this project.

### Dockerized App

To start both containers run on the cja-license-server:

`bash run.sh`

### Start on local

Create Virtual environment - Venv:
`python -m venv venv`

Activate Venv:

`source ./venv/bin/activate`

Then install the dependencies with:

`pip install -r requirements.txt`

#### Running tests (must be done with bash):

`bash test.sh`
