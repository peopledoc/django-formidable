=====
Forms
=====

The main purpose of this app is to handle Forms. Of course, the app provides an API to Create and Edit forms, but it's not the only option:
``django-formidable`` also provides a full python builder in order to create forms. ``django-formidable`` also provides a method to retrieve a standard django form class which can then be used just like an ordinary django form.


Formidable object
=================

The main class is :class:`formidable.models.Formidable`. This class is a classic django model which defines a representation of a dynamic form.

.. autoclass:: formidable.models.Formidable
    :members:

This is the main object which is used to create or edit dynamic forms through the RESTful API or directly in Python/Django.


Django form class
-----------------

One of the main feature is to provide a standard django form class built from the definition stored as Formidable object. The django form class is accessible throught the :meth:`formidable.models.Formidable.get_django_form_class`.

.. code-block:: python

    >>> formidable = Formidable.objects.get(pk=42)
    >>> form_class = formidable.get_django_form_class()


This form class can be manipulated as all django form class, you can build an instance to validate data:


.. code-block:: python

    >>> form = form_class(data={'first_name': 'Obiwan'})
    >>> form.is_valid()
    False
    >>> form.errors
    {'last_name': ['This field is required.']}
    >>> form = form_class(data={'first_name': 'Obiwan', 'last_name': 'Kenobi'})
    >>> form.is_valid()
    True


Or to render it:


.. code-block:: python

    {{ form.as_p }}


When a standard mechanism is implemented, you have a method to custom the final objec we get. ``django-formidable`` provides a way in order to custom the form class you get.

Each kind of field is built with an associated FieldBuilder:

==========    ======================================  ==========================================================
    slug                Field / Widgets                 FieldBuilder
==========    ======================================  ==========================================================
text           CharField / TextInput                    :class:`formidable.forms.field_builder.TextFieldBuilder`
paragraph      CharField / TextArea                     :class:`formidable.forms.field_builder.ParagraphFieldBuilder`
dropdown       ChoiceField / Select                     :class:`formidable.forms.field_builder.DropdownFieldBuilder`
checkbox       ChoiceField / CheckboxInput              :class:`formidable.forms.field_builder.CheckboxFieldBuilder`
radios         ChoiceField / RadioSelect                :class:`formidable.forms.field_builder.RadioFieldBuilder`
checkboxes     ChoiceField / CheckboxSelectMultiple     :class:`formidable.forms.field_builder.CheckboxesFieldBuilder`
email          EmailField / TextInput                   :class:`formidable.forms.field_builder.EmailFieldBuilder`
date           DateField                                :class:`formidable.forms.field_builder.DateFieldBuilder`
number         IntegerField                             :class:`formidable.forms.field_builder.IntegerFieldBuilder`
==========    ======================================  ==========================================================

So, as describe in django document (https://docs.djangoproject.com/en/1.9/topics/forms/media/#assets-as-a-static-definition), if you want add a CalendarWidget on the date field on your form, you can write your own field builder.


.. code-block:: python

    from django import forms

    from formidable.forms.field_builder import DateFieldBuilder, FormFieldFactory

    class CalendarWidget(forms.TextInput):

        class Media:
            css = {
                'all': ('pretty.css',)
            }
            js = ('animations.js', 'actions.js')


    class CalendarDateFieldBuilder(DateFieldBuilder):
        widget_class = CalendarWidget


    class MyFormFieldFactory(FormFieldFactory):
        field_map = FormFieldFactory.field_map.copy()
        field_map['date'] = CalendarDateFieldBuilder


With this definition you can call:

.. code-block:: python

    >>> formidable.get_django_form_class(field_factory=MyFormFieldFactory)

Roles and access-rights
=======================

Roles
-----

One of the main features of :mod:`formidable` is to set up different access-rights for the same form. This way, you can create a form with certain fields
that are only accessible to a specific group of users, for example.

For the moment, :mod:`formidable` is not designed to work without roles, so even if you don't need to handle multiple roles or access-rights inside your application, you will still have to define
a default role for :mod:`formidable` to work properly.

All roles must be declared through a :class:`formidable.accesses.AccessObject` instance. This class must be instantiated with an :attr:`id` and a :attr:`label`.
The :attr:`id` has to be unique, it's up to you to maintain this constraint. The :attr:`label` serves as a human readable value. You can set this to any string you like.

.. code-block:: python

    from formidable.accesses import AccessObject

    padawan = AccessObject(id='padawan', label='Padawan')
    jedi = AccessObject(id='jedi', label='Jedi')
    sith = AccessObject(id='sith', label='Bad Guy')



:mod:`django-formidable` needs to know how to get all declared instances. To do so, you will need to create a function which returns the correct instances:

.. code-block:: python

    def get_accesses():
        return [padawan, jedi, sith]


Once this function is defined, you will need to fill the settings key ``FORMIDABLE_ACCESS_RIGHTS_LOADER``.


.. code-block:: python

    FORMIDABLE_ACCESS_RIGHTS_LOADER = 'myapp.accesses.get_accesses'


Once this is done, :mod:`django-formidable` will know which roles have been defined, so it can create or check access-rights as necessary.


Fetch context
-------------
Occasionally, :mod:`django-formidable` will require access to the web request's context, e.g. to find out which kind of user is accessing the current form.

For this reason, you must define a function to fetch the context of the current request. The function takes as parameters the request object of the view (``self.request``)
and the view kwargs (``self.kwargs``).

The function must return an access id which is defined in one of the AccessObject instances returned by the method configured in ``FORMIDABLE_ACCESS_RIGHTS_LOADER``.

If the user's role is defined as an attribute, you can just return it directly:

.. code-block:: python

    def fetch_context(request, kwargs):
        return request.user.role


Then, set ``FORMIDABLE_CONTEXT_LOADER`` in your settings:


.. code-block:: python

    FORMIDABLE_CONTEXT_LOADER = myapp.accesses.fetch_context


Available access-rights
-----------------------

For each field of a form, and for each role you have defined, you can define a specific access-right.
There are four different available access-rights:

- ``EDITABLE``, the user may fill-in the field but there is no obligation to do so.
- ``REQUIRED``, the user must fill-in the field in order to submit the form.
- ``READONLY``, this will render the field as disabled, allowing the user to view but not modify its contents.
- ``HIDDEN``, the field will not be available to the user, preventing the user from either viewing or modifying its contents.

All the value are defined in :mod:`formidable.constants`

Conditions
==========

.. automodule:: formidable.forms.conditions

Python builder
==============

In some cases, you may want to build a formidable object without using the RESTful API (in tests for example). ``django-formidable`` provides a
Python API in order to that. Take a look at :mod:`formidable.forms.fields` to discover all the fields that are available through this API.

The main class to use is :class:`formidable.forms.FormidableForm`. Feel free to subclass this form and define your own form(s),
just like any other django form.

For example, let's say we need to build a form with a first name, last name and a description. We can use :mod:`formidable.fields`
to accomplish this. Lets consider using the different roles defined in the installation part, jedi and padawan.


.. code-block:: python


    from formidable.forms import FormidableForm
    from formidable.forms import fields


    class MySubscriptionForm(FormidableForm):

        first_name = fields.CharField(label='Your First Name')
        last_name = fields.CharField(label='Your Last Name')
        description = fields.TextField(
            label='Description',
            help_text='Tell us about yourself.'
        )


Attributes like ``required`` should not be used as these will depend on the context when the form is built. If you want to define a field as required, it will need to be required
for a specific role through the :attr:`accesses` argument. This argument is a dictionary containing the various access-rights for each role. By default, if you don't specify any access-rights
for a previously defined role, the field will be created as ``EDITABLE``:


.. code-block:: python

    class MySubscriptionForm(FormidableForm):

        first_name = fields.CharField(
            label='Your First Name',
            accesses={'padawan': constants.REQUIRED, 'jedi': constants.READONLY}
        )
        last_name = fields.CharField(label='Your Last Name')
        description = fields.TextField(
            label='Description',
            help_text='Tell us about yourself.'
        )


When the form definition is complete, you can create a new :class:`formidable.models.Formidable` object:


.. code-block:: python

    formidable = MySubscriptionForm.to_formidable(
        label='My Subscription Form',
        description='This form is for subscribing to the jedi order.')

This method will create the object in the database and return the complete instance:


.. code-block:: python

    >>> formidable.pk
    42

You can also get the django form class from the formidable object:

.. code-block:: python

    >>> form_class = formidable.get_django_form_class(role='padawan')

For our 'padawan' role, the first_name is required:

.. code-block:: python

    >>> form = form_class(data={'last_name': 'Kenobi'})
    >>> form.is_valid()
    False
    >>> form.errors
    {'first_name': ['This field is required.']}



Available fields
----------------

.. automodule:: formidable.forms.fields
    :members:


Available Widgets
-----------------

.. automodule:: formidable.forms.widgets
