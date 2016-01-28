# DesertAvalanche
Software Engineering Group Term Project - UNO CSCI 4830

In order to run the web server for our project, perform the following steps from a shell:

1) Get easy_install: (https://pypi.python.org/pypi/setuptools#unix-including-mac-os-x-curl)

    curl https://bootstrap.pypa.io/ez_setup.py -o - | python

2) Get pip:

    easy_install pip

3) Get Virtualenv:

    pip install virtualenv

4) Within the root working directory, set up virtual python environment:

    virtualenv --python=python2 env

5) Activate the virtualenv:

    source env/bin/activate

(to get out of the virtualenv, type:)

    deactivate

6) While the virtualenv is active, install requirements:

    pip install -r requirements.txt

7) To reset the database (in case you are starting out, messed something up, or changed the schema):

    python resetdb.py

8) Then, to start the server, run:

    python server.py

9) To see the web application, open a web browser, and type:

    localhost:5000
