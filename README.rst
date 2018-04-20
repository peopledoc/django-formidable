=================
django-formidable
=================

.. image:: docs/source/_static/formidable-logo.png

.. image:: https://circleci.com/gh/peopledoc/django-formidable.svg?style=svg&circle-token=6f273f564e1e44f702aef7c1d00baff74609c791
    :target: https://circleci.com/gh/peopledoc/django-formidable

django-formidable is a full django application which allows you to create,
edit, delete and use forms.

Warnings
========

* Python Compatibility : Python 2.7, 3.5, 3.6
* Django compatibility : Django 1.10, 1.11

See the `Deprecation timeline <http://django-formidable.readthedocs.io/en/latest/deprecations.html>`_ document for more information on deprecated versions.

.. warning::

   As of its 3.7 version, it appears that Django REST Framework only supports Django 1.10 & 1.11. Carefully freeze your dependencies if your Django version is not compatible.

License
=======

MIT License

Documentation
=============

Latest version of the documentation: http://django-formidable.readthedocs.io/en/latest/

If you want to build the documentation locally, you can try to run one of the following:

.. code:: sh

    $ make docs
    $ tox -e docs

.. note::

    A recent version of `tox` must be available on your system.

You can also browse the documentation locally, using the following, for example:

.. code:: sh

    $ make docs serve-docs

Quick-Start
===========

Install
-------

.. code:: sh

    $ pip install django-formidable

Configure
---------

Define Roles
~~~~~~~~~~~~

django-formidable allows access to a single form by different roles.
The same form can thus be rendered in different ways. If you don't need
to handle multiple roles you must still define at least one default role.

Define a method which returns a list of formidable.accesses.AccessObject:

.. code-block:: python

    def get_roles(self):
        return [
            AccessObject(id='padawan', label='Padawan'),
            AccessObject(id='jedi', label='Jedi')
        ]

Fill the settings key:

.. code-block:: python

    FORMIDABLE_ACCESS_RIGHTS_LOADER = 'yourproject.access_rights.get_roles'

Get context
~~~~~~~~~~~

While accessing a form for a specific role, you need to provide a way in
which to get the correct context to use.

``request`` and ``kwargs`` are fetched from the view (self.request,
self.kwargs)

.. code-block:: python

    def get_context(request, kwargs):
        return request.user.user_type

Next fill the setting key ``FORMIDABLE_CONTEXT_LOADER``

.. code-block:: python

    FORMIDABLE_CONTEXT_LOADER = 'yourprojects.access_rights.get_context'

Define URLs
-----------

URLs are defined in ``formidable.urls``. You can load them with the
following line:

.. code-block:: python

    url(r'^api/', include('formidable.urls', namespace='formidable'))


By default, the views are not accessible, the permissions loaded are fully
restrictive. To allow any access to the view fill your settings with

.. code-block:: python

    FORMIDABLE_DEFAULT_PERMISSION=['rest_framework.permissions.AllowAll']


To handle special permissions, please refer to the online documentation.
