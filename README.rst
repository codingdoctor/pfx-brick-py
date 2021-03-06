PFx Brick Python API
====================

.. image:: https://travis-ci.org/fx-bricks/pfx-brick-py.svg?branch=master
    :target: https://travis-ci.org/fx-bricks/pfx-brick-py
.. image:: https://img.shields.io/pypi/v/pfxbrick.svg
    :target: https://pypi.org/project/pfxbrick/
.. image:: https://img.shields.io/badge/license-MIT-blue.svg 
    :target: https://github.com/fx-bricks/pfx-brick-py/blob/master/LICENSE.md


This repository contains the API for developing python scripts and applications which communicate with the PFx Brick.

Getting Started
===============

Requirements
------------

* Python 3.6+
* hidapi
* sphinx (for documentation)

Installation
------------

The **pfxbrick** package can be installed with pip:

.. code-block:: shell

    $ pip install pfxbrick
    
or directly from the source code:

.. code-block:: shell

    $ git clone https://github.com/fx-bricks/pfx-brick-py.git
    $ cd pfx-brick-py
    $ python setup.py install

Basic Usage
===========

After installation, the package can imported:

.. code-block:: shell

    $ python
    >>> import pfxbrick
    >>> pfxbrick.__version__

An example of the package can be seen below

.. code-block:: python

    from pfxbrick import PFxBrick

    # Open a PFx Brick session instance
    brick = PFxBrick()
    brick.open()
    
    # Get the status and identity of the PFx Brick
    print('PFx Brick ICD version : %s' %(brick.get_icd_rev()))
    brick.get_status()
    brick.print_status()
    
    # Get the PFx Brick configuration settings
    brick.get_config()
    brick.print_config()
    
    # Get the user defined name of the PFx Brick
    brick.get_name()
    print(brick.name)
    
    # Change the user defined name
    brick.set_name('My Cool Brick')
    
    # End the session
    brick.close()


---------------

Documentation
=============

* `PFx Brick Interface Control Document (ICD) v.3.36 <https://github.com/fx-bricks/pfx-brick-dev/raw/master/doc/ICD/PFxBrickICD-Rev3.36.pdf>`_ describes details of PFx Brick operation and communication protocol
* `Python API Reference Documentation <https://www.fxbricks.com/docs/python/index.html>`_ 

If you want to learn more about PFx Brick, check out `our website <https://fxbricks.com/pfxbrick>`_.

 