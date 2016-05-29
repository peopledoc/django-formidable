Forms
+++++

The main purpose of this app is to handle Forms. Of course, the app provides an API way to Create and Edit forms. But it's not the only way.
``django-formidable`` provides a full python builder in order to create form. Moreover, when a form is created it's really usefull to get it
as standard django form. For this, ``django-formidable`` provides a method to get this standard django form class and use it as normal django form.


Formidable object
=================

The main class is :class:`formidable.models.Formidable`. This class is a classic django model which defines a representation of dynamic form.

.. autoclass:: formidable.models.Formidable
    :members:

This is the main object manipulated in order to create or edit dynamic form through RESTful API or python/django.


Django form class
-----------------

One of the main feature is to provide a standard django form class built from the definition stored as Formidable object. The django form class is accessible throught the :meth:`formidable.models.Formidable.get_django_form_class`.

.. code-block:: python

    >>> formidable = Formidable.objects.get(pk=42)
    >>> form_class = formidable.get_django_form_class()


This form class can be manipulated as all django form class, you can build an instance to validate data


.. code-block:: python

    >>> form = form_class(data={'first_name': 'Obiwan'})
    >>> form.is_valid()
    False
    >>> form.errors
    {'last_name': ['This field is required.']}
    >>> form = form_class(data={'first_name': 'Obiwan', 'last_name': 'Kenobi'})
    >>> form.is_valid()
    True


Or to render it


.. code-block:: python

    {{ form.as_p }}


When a standard mechanism is implemented, you have a method to custom the final objec we get. ``django-formidable`` provides a way in order to custom the form class you get.

Each kind of field is built with an associated FieldBuilder

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


With this definition you can call

.. code-block:: python

    >>> formidable.get_django_form_class(field_factory=MyFormFieldFactory)

Roles and Accesses
==================

Roles definition
----------------

One of the main features of :mod:`formidable` is to provide different accesses on the same form. With this, you can create a form with "admininstration part"
with different access level for example.

For the moment, :mod:`formidable` is not designed to work without roles, so even if you haven't to handle multiple roles or accesses inside your application, you have to define
a default role.

All role has to be declared throught :class:`formidable.accesses.AccessObject` instance. This class is really simple, it has to be created with an :attr:`id` and a :attr:`label`.
The :attr:`id` has to be uniq, it's up to you to keep it with this constraint. The :attr:`label` is here to for human readable value. You can put what you want in it.

.. code-block:: python

    from formidable.accesses import AccessObject

    padawan = AccessObject(id='padawan', label='Padawan')
    jedi = AccesObject(id='jedi', label='Jedi')
    sith = AccesObject(id='sith', label='Bad Guy')



:mod:`django-formidable` needs to know how to get all declared instancies. To do it , you have to create a function which returns the instances.

.. code-block:: python

    def get_accesses():
        return [padawan, jedi, sith]


Once your function is declared you have to fill the settings key ``FORMIDABLE_ACCESSES_LOADER``.


.. code-block:: python

    FORMIDABLE_ACCESSES_LOADER = 'myapp.accesses.get_accesses'


With this, :mod:`django-formidable` is able to know which roles you defined and create or check related accesses when needed.


Fetch Context
-------------

For some view, :mod:`django-formidable` needs to know how to fetch the context of the web request, e.g. which kind of user is accessing the current form.
You need to define a function to fetch the context of the current request. The function takes as parameters the request object of the view (``self.request``)
and the view kwargs (``self.kwargs``).

The function as to retur the an access id which is define in one the AccessObject instance returned by the method configured in ``FORMIDABLE_ACCESSES_LOADER``

If the user's role is defined in a attribut, you can just return it.

.. code-block:: python

    def fetch_context(request, kwargs):
        return request.user.role


Then, fill the settings key ``FORMIDABLE_CONTEXT_LOADER``


.. code-block:: python

    FORMIDABLE_CONTEXT_LOADER = myapp.accesses.fetch_context


Available accesses
------------------

For each field of a form, and for each role you defined, you can define a specific access.
There are four different available access

- ``EDITABLE``, the user is allow to fill the field but it is not required.
- ``REQUIRED``, define the field as required, the user has to fill the field.
- ``READ_ONLY``, disable the field on the display and the user can not fill the field.
- ``HIDDEN``, the field is not available for the user , he cannot fill it.


Python builder
==============

For some reasons, you may want to build a formidable object without the RESTful API (tests for example). ``django-formidable`` provides a
python API in order to that. You can have a look on the :mod:`formidable.forms.fields` to know all the fields are available for
this kind of definition.
The main class to use is :class:`formidable.forms.FormidableForm`. You can subclasse this definition and define your own form
like any django form.

For example, you need to build a form with a first name, last name and a description of what you need. Use :mod:`formidable.fields`
in order to do that. Lets consider using the different roles defined in the installation part, jedi and padawan.


.. code-block:: python


    from formidable.forms import FormidableForm
    from formidable.forms import fields


    class MySubscriptionForm(FormidableForm):

        first_name = fields.CharField(label='Your First Name')
        last_name = fields.CharField(label='Your Last Name')
        description = fields.TextField(label='Description', help_text='Write a text about you.'),


Attribute like ``required`` are not used on this definition because is depends on the context the form is build. So If you want to define a field as required, it has be required
for a specific role through :attr:`accesses` argument. This argument is a dictionary containing the different access for different role. By default, if you don't specify any access
for role previously defined, the access for the role is created as ``EDITABLE``


.. code-block:: python

    class MySubscriptionForm(FormidableForm):

        first_name = fields.CharField(label='Your First Name', accesses={'padawan': 'REQUIRED', 'jedi': 'READ_ONLY'})
        last_name = fields.CharField(label='Your Last Name')
        description = fields.TextField(label='Description', help_text='Write a text about you.'),


When the definition is complete you can create a :class:`formidable.models.Formidable` object


.. code-block:: python

    formidable = MySubscriptionForm.to_formidable(label='My Subscription Form', description='This is a form in order to subscribe to jedi order.')

This method will create the object in database and return the complete instance.


.. code-block:: python

    >>> formidable.pk
    42

And you can get the final django form class from the formidable object

.. code-block:: python

    >>> form_class = formidable.get_django_form_class(role='padawan')

For padawan role, the first_name is required

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
