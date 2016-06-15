Install
+++++++

Install the app
===============


From Github
-----------

For the moment, no release is available on the PyPi, but you can install it from github

.. code-block:: sh

    pip install git+https://github.com/peopledoc/django-formidable.git


From PyPI
---------

TODO: Coming soon.


Configure the app
=================

Before you can use the app, some things need to be configured in order
to get it fully operational. :mod:`django-formidable` has the ability to handle
different roles and accesses on a per form basis. This is useful when you have
multiple types of user accessing the same form. If you don't need multiple roles,
just create a single unique role, this will be enough.


Configure access-rights
-----------------------

First of all, you need to declare all available roles inside your application.
To do this, create an :class:`formidable.accesses.AccessObject` per role needed.

.. code-block:: python

    from formidable.accesses import AccessObject

    jedi = AccessObject(id='jedi', label='Jedi')
    padawan = AccessObject(id='padawan', label='Padawan')


Once your roles are defined, you will need to create a function to return them,
in your projects (for the purposes of this example, we're assuming the function
will be created in the module ``yourproject.access_rights``):

.. code-block:: python

    def get_access_rights():
        return [jedi, padawan]


The main idea is to create a function which can be called by :mod:`django-formidable`
to get the declared roles you defined previously. To tell :mod:`django-formidable`
where the function is located, you need to add ``FORMIDABLE_ACCESS_RIGHTS_LOADER``
to your settings:

.. code-block:: python

    FORMIDABLE_ACCESS_RIGHTS_LOADER = 'yourproject.access_rights.get_access_rights'


Fetch the context
-----------------

When the content of a contextualised form are required, e.g. to render it in
a JavaScript front-end, :mod:`django-formidable` needs to know which context
to fetch in order to render the correct fields with the right permissions.

To do this, we'll need to write some code which will be called by
:mod:`django-formiable`.

Let's assume your user model has a ``user_type`` attribute on it. In this case,
you could write the following function:

.. code-block:: python

    def get_context(request, kwargs):
        return request.user.user_type


The :attr:`request` is a standard Django request, as found in any view.
Likewise, :attr:`kwargs` is a standard dictionary of keyword arguments.
Of course, the user type should correspond to the ``id`` of the AccessObject

Next fill the setting key ``FORMIDABLE_CONTEXT_LOADER``

    FORMIDABLE_CONTEXT_LOADER = 'yourproject.access_rights.get_context'


Formidable's URLs
-----------------

URLs are defined in :mod:`formidable.urls`. You can load them with the
following line:

.. code-block:: python

    url(r'^api/', include('formidable.urls', namespace='formidable'))
