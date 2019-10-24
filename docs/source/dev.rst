=========================
Developer's documentation
=========================

Testing
-------

Prerequisites
~~~~~~~~~~~~~

If you want to run the whole test suite, you'll need to have a working Postgresql server instance (preferrably the latest), with the ``pg_virtualenv`` tool available.
On Debian, this executable is provided by the package ``postgresql-common``.

If you don't have this tools in your toolbox, then... if you're doing a change that **impacts the performance records**, you won't be able to see or generate the diff, **so your branch tests would fail.**

.. note::

    Postgresql driver is only available for Linux or MacOS.

Using tox
~~~~~~~~~

Tests are launched using `tox <http://tox.readthedocs.io/>`_. You may want to become proficient with this tool but the core command you need to know is:

.. code:: shell

    $ tox

This will run all the test suite, for all the versions of Django, using all the Python interpreters supported.

Targeting a specific environment is done using:

.. code:: shell

    $ tox -e django111-py27

If you want to target a specific test, simply add its namespace after a double-dash ``--``.

For example, the following will run ``test_fields`` test module using Django 1.11 and Python 2.7:

.. code:: shell

    $ tox -e django111-py27 -- tests.test_fields

And the following will run the same test class for all the supported environments:

.. code:: shell

    $ tox -- tests.test_fields.RenderingFormatField

If somehow you've messed-up with your environment(s), you can still recreate it/them using:

.. code:: shell

    $ tox -r  # RECREATE ALL THE THINGS
    $ tox -re django111-py27  # recreate and run tests using `django111-py27`


Using py.test
~~~~~~~~~~~~~

You can also run tests with ``py.test``.

You can install it with the following command:

.. code:: shell

    $ pip install pytest{,-django}
    # Optionally
    $ pip install pytest-sugar

We've added a section in our ``setup.cfg``, so you should be able to run tests simply with:

.. code:: shell

    $ cd demo/
    $ py.test


Swagger documentation update
----------------------------

If at any point you've changed something in the :file:`docs/swagger/formidable.yml` file, you'll **have** to run the following to refresh at least the :file:`docs/source/_static/specs/formidable.js` file that will be used in the :doc:`api` document.

Run the following to regenerate all the necessary statics:

.. code:: shell

    $ tox -e swagger-statics

and commit the diffs in your PR.
