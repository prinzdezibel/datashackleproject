datashackleproject sets up a skeleton for building datashackle web applications.
In order to do so, we are approaching a `buildout-based <http://www.buildout.org>`_ installation.

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

The next steps are optional. You may execute it if you experience problems
with your python environment::

  $ virtualenv --no-site-packages .
  $ source bin/activate

Bootstrap your buildout::

  $ python bootstrap.py

Now you can run the buildout::

  $ bin/buildout

Now you can start the newly created app. Ensure that the mysql server is 
up and running::

  $ bin/paster serve parts/etc/debug.ini


Point your browser to ``http://localhost:8080``