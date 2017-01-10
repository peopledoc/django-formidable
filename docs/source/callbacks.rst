=========
Callbacks
=========

.. versionadded:: 0.5

Each time a formidable form is created or updated, the API views are able to call a function that can help you trigger actions. For example, you can use the :mod:`django.contrib.messages` to inform your current user that their form has been successfully saved or that a problem has occurred ; or send an email or ping an API, or... whatever you want.

By default, the view won't load and launch anything. In order to set a callback up, you'll need to give a value to any of the following variables:

* ``FORMIDABLE_POST_CREATE_CALLBACK_SUCCESS``: callback to call when form creation is successful.
* ``FORMIDABLE_POST_CREATE_CALLBACK_FAIL``: callback to call when form creation has failed.
* ``FORMIDABLE_POST_UPDATE_CALLBACK_SUCCESS``: callback to call when form update is successful.
* ``FORMIDABLE_POST_UPDATE_CALLBACK_FAIL``: callback to call when form update has failed.

The callback functions
----------------------

A callback function is a function that accepts only one argument, the `request` object coming from the API View. It doesn't have to return anything, it can make multiple calls... it's up to you.

.. code-block:: python

    def callback_on_success(request):
        mail.send(request.user.email, 'All is fine')

.. warning::

    the DRF request is not inherited from django core, :class:`HTTPRequest`, and you should not assume they'll behave the same way. It shares some properties, so it may quack like a duck, but it's not a duck.

    If you need the "true" HTTPRequest object, use ``self.request._request``. That might be the case if you want to use the :mod:`django.contrib.messages`.

    .. code-block:: python

        def callback_on_success(request):
            messages.info(request._request, "Your form is recorded")

Fails silently
--------------

At the moment, if your callback fails for some reason and throws an exception, the exception is logged and the error is skipped. We've decided not to re-raise the exception to avoid your database transaction to be rolled back and the form you've tried to save being lost. After all, it's not the users fault if the callback has failed, but the integrator's.

At some point, we may add a "fail" mode and re-raise the exception and allow the integrator to make sure that the DB transaction is either committed if everything is fine, or aborted if something bad happened in the callback function.
