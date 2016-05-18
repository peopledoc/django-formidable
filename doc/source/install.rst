Install
+++++++

Install the app
===============

from Pypi

.. code-block:: sh

    pip install django-formidable


The installation part from github is coming later.


Configure the app
=================

In order to get the app ready to use, you have couple things to do before
to get it operational. :mod:`django-formidable` has the ability to handle
different roles and accesses per forms. It usefull when you have multiple kind
of user access the same form. If you don't have multiple role to handle, just
create a unique role, it will be enough.


Configure accesses
------------------

First of all, you have to declare available role inside your application. To do
this, create one :class:`formidable.accesses.AccessObject` per role you need.

.. code-block:: python

    from formidable.accesses import AccessObject

    jedi = AccessObject(id='jedi', key='Jedi')
    padawan = AccessObject(id='padawan', label='Padawan')


Once your roles have been defined create a function to return its, in your
projects. (Considering the function is created in module yourproject.accesses)

.. code-block:: python

    def get_accesses():
        return [jedi, padawan]


The main idea is to create a function can be called by :mod:`django-formidable`
to get the declared roles you defined previously. To tell to django-formidable
where the function is you have to add a settings ``FORMIDABLE_ACCESSES_LOADER``

.. code-block:: python

    FORMIDABLE_ACCESSES_LOADER = 'youproject.accesses.get_accesses'


Fetch the context
-----------------

When accessing in the javascript form renderer, :mod:`django-formidable` has
to know which context to fetch in order to render the right fields with the
right permissions

To do this, we need to write a piece of code wich will be called by
:mod:`django-formiable`.

Imagine your actual user has an attribute to know which kind of user he is.
You can right a function like this.

.. code-block:: python

    def get_context(request, kwargs):
        return request.user.user_type


The :attr:`request` is the usual django request you can find in the view. It's
the same for :attr:`kwargs` arguments.
Of course, the user type has to be the ``id`` of the AccessObject you defined
previously.


Formidable's URLs
-----------------

Url's are define in :mod:`formidale.urls`, in order to use it, you can load it
with:

.. code-block:: python

    url(r'^api/', include('formidable.urls', namespace='formidable'))
