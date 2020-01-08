==============
Security setup
==============

As any other web application, Django Formidable might be targeted by pirates who would try to inject SQL or malicious code through Javascript or any other XSS method.

How to secure your django-formidable installation
=================================================

Add the following settings: ``DJANGO_FORMIDABLE_SANITIZE_FUNCTION``. It should be a string that points at a function.

.. important::

    We highly recommend to use `bleach <https://pypi.org/project/bleach/>`_, with dedicated adjustments in order to make sure you're sanitizing your content in a proper way.

    See `bleach documentation <https://bleach.readthedocs.io/en/latest/>`_ for creating your own parameters when calling the ``clean()`` function.

Example
=======

In your :file:`settings.py`, add the following:

.. code-block:: python

    DJANGO_FORMIDABLE_SANITIZE_FUNCTION = "path.to.module.clean_func"

And then in the :file:`path/to/module.py` module, add a function that would look like this:

.. code-block:: python

    import bleach

    def clean_func(obj):
        """
        Sanitize API text content
        """
        return bleach.clean(obj, strip=True)

.. warning::

    If you don't add this settings or if its value is not importable (typo, missing PYTHONPATH, etc.):

    * an error log will be raised,
    * django-formidable won't sanitize your contents for you.

Secured fields
==============

* Form label & description,
* Field label, description (help text), defaults, placeholder.
