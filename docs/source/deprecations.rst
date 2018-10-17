====================
Deprecation timeline
====================

From 2.1.2 to 3.0.0
===================

Octobre 31st, 2018

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
