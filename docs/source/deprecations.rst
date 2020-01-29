====================
Deprecation timeline
====================

From 4.0.1 to x.y.z
===================

.. deprecated:: x.y.z

    Drop support for Django Rest Framework 3.8

.. versionchanged:: x.y.z

    Replaced ``jsonfield`` library by ``jsonfield2``.

.. warning::

    **Important Warning for Integrators**: ``jsonfield`` and ``jsonfield2`` are using the same namespace. So if you are migrating to this version, you'll probably have to make sure that ``jsonfield`` package is totally removed from your environment before using django-formidable.


From 3.3.0 to 4.0.0
===================

Jan 8th, 2020.

Python versions
---------------

.. deprecated:: 4.0.0

    Drop support for Python 2.7 (EOL is January 1st, 2020)

Configuration option
--------------------

.. versionadded:: 4.0.0

    Added support for XSS prevention using the ``DJANGO_FORMIDABLE_SANITIZE_FUNCTION`` settings. See `the security Documentation <https://django-formidable.readthedocs.io/en/master/security.html>`_ for more information.


From 3.2.0 to 3.3.0
===================

Django versions
---------------

.. versionadded:: 3.3.0

    Added support for Django 2.2. Django Formidable should probably work on Django 2.0 and 2.1, but it's not in our test suite. We've decided to skip those versions because of their short-term support.

Python versions
---------------

.. versionadded:: 3.3.0

    Added support for Python 3.7 and 3.8


From 3.1.0 to 3.2.0
===================

November 7th, 2019

Django versions
---------------

.. deprecated:: 3.2.0

    Drop support for Django 1.10 (EOL was in December 2nd, 2017)

From 3.0.1 to 3.1.0
===================

June 3rd, 2019

Django REST Framework versions
------------------------------

.. versionadded:: 3.1.0

    Support for Django REST Framework on all versions up to the 3.9 series.


From 2.1.2 to 3.0.0
===================

October 31st, 2018

Django REST Framework versions
------------------------------

.. deprecated:: 3.0.0

    Support for Django REST Framework stricly greater than 3.8.
    The 3.9 series has introduced an incompatibility with ``django-formidable``.


From 1.7.0 to 2.0.0
===================

(end of May 2018)

Django versions
---------------

.. deprecated:: 2.0.0

    Support for Django 1.8 & 1.9.

Crowdin
-------

.. deprecated:: 2.0.0

  The Django Formidable project doesn't handle any translatable string anymore.


From 1.3.0 to 1.4.0
===================

Validation endpoint
-------------------

.. deprecated:: 1.4.0

    Validation endpoint for **user data** doesn't allow GET method anymore.

From 0.15 to 1.0.0
==================

(September 2017)

Form Presets
------------

.. deprecated:: 1.0.0

    Form presets will be deprecated in favor of Field validation rules. If needed, you'll have to convert your existing Presets to Field validations, because Presets data will be destroyed using a table deletion.

Django Rest Framework version
-----------------------------

.. deprecated:: 1.0.0

    DRF 3.3 support will be deprecated. We recommend to use the latest to date (3.6.4).

From 0.11.1 to 0.12.0
=====================

.. deprecated:: 0.12.0

    Python 3.4 support has been dropped.


From 0.8.2 to 0.9
=================

.. deprecated:: 0.9

    Python 3.3 support has been dropped.
