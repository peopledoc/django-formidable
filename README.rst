=================
django-formidable 
=================

.. image:: https://raw.githubusercontent.com/novafloss/django-formidable/master/formidable.png

.. image:: https://circleci.com/gh/novafloss/django-formidable.svg?style=svg&circle-token=6f273f564e1e44f702aef7c1d00baff74609c791
    :target: https://circleci.com/gh/novafloss/django-formidable

django-formidable is a full django application which allows you to create,
edit, delete and use forms.

Warning
=======

Python Compatibility : python2.7 (tox says it's compliant up to
python3.2, but I don't)
Django compatibility : django1.8

It's not production-ready yet, and no official version has currently
been released on PyPI.

Licence
=======

MIT Licence

Documentation
=============

Latest version of the documentation http://django-formidable.readthedocs.io/en/latest/

Quick-Start
===========

Install
-------

No release is yet available, but it can be installed via github.

::

    $ sudo pip install git+https://github.com/novafloss/django-formidable.git

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



formidable-ui
-------------

Plug in formidable-ui

https://github.com/peopledoc/formidable-ui#integration
