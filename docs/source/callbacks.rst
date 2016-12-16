=========
Callbacks
=========

Each time a formidable form is created or updated, the API views are able to call a function that can help you trigger actions. For example, you can use the :mod:`django.contrib.messages` to inform your current user that their form has been successfully saved or that a problem has occurred ; or send an email or ping an API, or... whatever you want.

By default, the view won't load and launch anything. In order to set a callback up, you'll need to give a value to any of the following variables:

* ``FORMIDABLE_POST_CREATE_CALLBACK_SUCCESS``: callback to call when form creation is successful.
* ``FORMIDABLE_POST_CREATE_CALLBACK_FAIL``: callback to call when form creation has failed.
* ``FORMIDABLE_POST_UPDATE_CALLBACK_SUCCESS``: callback to call when form update is successful.
* ``FORMIDABLE_POST_UPDATE_CALLBACK_FAIL``: callback to call when form update has failed.
