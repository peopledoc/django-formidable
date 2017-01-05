=======
Install
=======

Install the app
===============


From PyPI
---------

.. code-block:: sh

    $ pip install django-formidable

From Github
-----------

You can also install ``django-formidable`` via GitHub:

.. code-block:: sh

    pip install git+https://github.com/peopledoc/django-formidable.git


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
:mod:`django-formidable`.

Let's assume your user model has a ``user_type`` attribute on it. In this case,
you could write the following function:

.. code-block:: python

    def get_context(request, kwargs):
        return request.user.user_type


The :attr:`request` is a standard Django request, as found in any view.
Likewise, :attr:`kwargs` is a standard dictionary of keyword arguments.
Of course, the user type should correspond to the ``id`` of the AccessObject

Next fill the setting key ``FORMIDABLE_CONTEXT_LOADER``:

.. code-block:: python

    FORMIDABLE_CONTEXT_LOADER = 'yourproject.access_rights.get_context'


Formidable's URLs
-----------------

URLs are defined in :mod:`formidable.urls`. You can load them with the
following line:

.. code-block:: python

    url(r'^api/', include('formidable.urls', namespace='formidable'))


URLs accesses
-------------

The ``Formidable`` views are built with ``djangorestframework`` and use the
related permissions in order to handle accesses. So, you can write your
own permissions with ``djangorestframework`` and use it in ``django-formidable``
views.


By default, a restrictive permission is applied on all API views if nothing is
specified in django settings.

You can specified a list of permissions classes to all the API views by
providing the configuration key ``FORMIDABLE_DEFAULT_PERMISSION``:

.. code-block:: python

    FORMIDABLE_DEFAULT_PERMISSION = ['rest_framework.permissions.AllowAll']


There are two kinds of views,

1. views which allow to create or edit forms (handled
by ``FORMIDABLE_PERMISSION_BUILDER``)
2. views to use the form previously defined (handled by.
``FORMIDABLE_PERMISSION_USING``).

You can provide any permissions you want.

CSRF
----

If you're dealing with logged-in users (you surely do), you're going to need to provide a CSRF Token when validating a creation or an edit form. If you don't provide it *or* if your CSRF is misconfigured, you'll receive a ``403`` error when trying to save your forms.

In order to do so, you'll have to use a code similar to this:

.. literalinclude:: ../../demo/demo/builder/static/assets/csrftoken.js
    :language: js

.. warning:: you'll have to make sure that your CSRF configuration is properly set (middlewares, context managers, etc).

Then in your templates, those that'll have to display and handle the form editor, you'll have to call this function like this:

.. code-block:: django

    <script src="{% static "assets/csrftoken.js" %}"></script>
    <script type="text/javascript">
        $(document).ready(function() {
            setupCRSFToken('{{ csrf_token }}');
        });
    </script>

This way, every AJAX call coming from this template will provide a token that'll fit Django's (and Django REST Framework) requirements.
