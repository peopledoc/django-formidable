=================
django-formidable
=================

django-formidable is a full django application allows you to create,
edit, delete and use forms.

Warning
=======

Python Compatibility : python2.7 (tox said it's compliant until
python3.2, but I don't) Django compatibility : django1.8

It's not prod-ready for the moment, no version has been released on
official Pypi.

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

No release is available, but we can install it from github.

::

    $ sudo pip install git+https://github.com/novafloss/django-formidable.git

Configure
---------

Define Roles
~~~~~~~~~~~~

django-formidable allows to access a single form with different role.
The same form can be rendered in different way. If you don't have to
handle multiple roles you have to define at least a default role.

Define a method which returns a list of formidable.accesses.AccessObject

.. code-block:: python

    def get_roles(self):
        return [
            AccessObject(id='padawan', label='Padawan'),
            AccessObject(id='jedi', label='Jedi')
        ]

Fill the settings key

.. code-block:: python

    FORMIDABLE_ACCESS_RIGHTS_LOADER = 'yourproject.access_rights.get_roles'

Get context
~~~~~~~~~~~

While accessing a form for a specific role, you need to provide a way in
order to get the which context to use.

``request`` and ``kwargs`` are fetch from view (self.request,
self.kwargs)

.. code-block:: python

    def get_context(request, kwargs):
        return request.user.user_type

Next fill the setting key ``FORMIDABLE_CONTEXT_LOADER``

.. code-block:: python

    FORMIDABLE_CONTEXT_LOADER = 'yourprojects.access_rights.get_context'

Define URL's
------------

URLs are defined in ``formidable.urls``. You can load them with the
following line:

.. code-block:: python

    url(r'^api/', include('formidable.urls', namespace='formidable'))
    
    

formidable-ui
-------------

Plug in formidable-ui 

https://github.com/peopledoc/formidable-ui#integration

