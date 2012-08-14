datashackleproject sets up a skeleton for building datashackle web applications.
In order to do so, we are approaching a `buildout-based <http://www.buildout.org>`_ installation.


**DISCLAIMER**
This software is a prototype and not suitable for anything other than for demonstration purposes.

**Prerequisites**
OS: Linux or OS X, no Windows
Browser: Only Firefox is supported
MySQL server installation
Python 2.6 or 2.7


**Install the required system packages**

Before even getting the source code, we need to make sure you have all the
system level dependencies installed. The following command will take care of it
when working with a debian linux. This may look a bit different, if you
use another linux disto::

  $ sudo apt-get install python-virtualenv python-dev libxslt1-dev libxml2-dev
  $ sudo apt-get install python-pip libmysqlclient-dev 

Install PasteScript::
  $ pip install PasteScript

**Installation and usage of datashackleproject**

The first thing to get started with a new datashackle project is to install
the datashackleproject package, which provides a PasteScript template to create
a buildout that sets up the environment for your new project::

  $ pip install datashackleproject

Afterwards you can run the ``datashackle`` script with the name of the
project you'd like to create as an argument::

  $ paster create -t datashackle myFirstDatashackleApp

You want to answer the questions when prompted. They are there to set intial
project configuration values. These can be changed later again.

Change to your project directory::

  $ cd myFirstDatashackleApp

Double check the database connection parameters
  $ vim buildout.cfg


The next steps are optional. You may execute it if you experience problems
with your python environment::

  $ virtualenv --no-site-packages .
  $ source bin/activate

Bootstrap your buildout::

  $ sudo python bootstrap.py

Now you can run the buildout::

  $ bin/buildout

Ensure that the mysql server is running and can be reached with the credentials you entered earlier.
Populate database with initial data:
  $ bin/migrate upgrade

Now you can start the newly created app.
  $ bin/paster serve parts/etc/debug.ini



Point your browser to ``http://localhost:8080``
