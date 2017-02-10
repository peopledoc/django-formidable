============
Translations
============

.. attention:: unless specified, what follows is for the core developer team of Formidable. The project translation process is in the making, so bear with us.

The Crowdin URL is: https://crowdin.com/project/django-formidable/
At the moment, it's a private crowdin project, but we'll open it to contributors as soon as possible.

Crowdin support
===============

If you're a core django-formidable contributor, you may have access to the Crowdin project. If so, then you have access to the API Key via the Settings Menu -> API tab.

To set up your crowdin environment, you'll have to do the following:

1. copy-paste the value of the API key in a file named :file:`.crowdin-cli-key`
2. run the following command:

.. code-block:: shell

    make crowdin-build-yaml

It'll build (or rebuild) the :file:`crowdin.yaml` configuration file.

You can now eventually build the "crowdin-enabled" virtualenv with:

.. code-block:: console

    make crowdin-venv

This virtualenv lives in the ``.crowdin`` directory. If you want to check your setup, you can run the following command and see an output that'd look like this:

.. code-block:: console

    $ .crowdin/bin/crowdin-cli-py list translations
    InsecurePlatformWarning [snip snip snip]
    en_GB/LC_MESSAGES/django.po
    fr/LC_MESSAGES/django.po
    de/LC_MESSAGES/django.po
    nl/LC_MESSAGES/django.po
    nb/LC_MESSAGES/django.po
    en_US/LC_MESSAGES/django.po
    tr_TR/LC_MESSAGES/django.po
    it/LC_MESSAGES/django.po
    zh_CN/LC_MESSAGES/django.po
    pt_BR/LC_MESSAGES/django.po
    es/LC_MESSAGES/django.po
    pl_PL/LC_MESSAGES/django.po

.. danger::

    It's important to NEVER EVER commit and push the API Key anywhere. It's **like a password** and it gives *full access* to the formidable project data and can even make **changes** in the project settings.

Use cases
=========

Here are the different use-cases that may occur about the project translation, and how to tackle them.


So you've changed / added / removed translatable strings
--------------------------------------------------------

.. note:: Available to any contributor


You'll have to generate the .po files and make them available in the code. If you are a contributor, you can generate it in your pull-request.

Run this command:

.. code-block:: console

    make gettext-makemessages

Variant: with a Crowdin access
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have access to crowdin via its API, you can make sure that the ``makemessages`` command will be executed for all the available languages using this command:

.. code-block:: console

    make crowdin-gettext-makemessages

This will call the API to list available languages, update the ``.po`` files for languages that were already there, and eventually create the missing ``.po`` files.


.. tip::

    This handy command would also help you create the ``.po`` files for a new language added to crowdin.

So you want to upload updated translatable strings to crowdin
-------------------------------------------------------------

.. note::

    Target: core contributor

Now that your ``.po`` files have been updated, you may want to push them to crowdin.com. Simply run this:

.. code-block:: console

    make crowdin-upload


You know that new strings are available on crowdin
--------------------------------------------------

.. note::

    Target: core contributor

Eventually, somebody has provided translations, (new or updated). You need to download them and update the ``.po`` files accordingly.

.. code-block:: console

    make crowdin-download

You want updated translations to be available in your applications
------------------------------------------------------------------

.. note:: Available to any contributor

You surely know that you need to compile all your ``.po`` files into ``.mo`` so gettext can pick them up.

.. code-block:: console

    make gettext-compile

.. tip:: you can download **AND** compile the whole thing using the ``make crowdin-download-compile`` Makefile target.
