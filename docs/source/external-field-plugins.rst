===============================
External Field Plugin Mechanism
===============================

We've included a mechanism to add your own fields to the collection of available fields in ``django-formidable``.

It'll be possible to:

* define a new form using this new type of field,
* store their definition and parameters in a Formidable object instance (and thus, in the database),
* using this form definition, validate the end-user data when filling this form against your field business logic mechanism.

For the sake of the example, let's say you want to add a "Color Picker" field in django-formidable. You'll have to create a django library project that we'll call ``django-formidable-color-picker``. Let's say that this module has its own ``setup.py`` with the appropriate scripts to be installed in dev mode using ``pip install -e ./``.

Let's also say that you have added it in your ``INSTALLED_APPS``.

Tree structure
==============

::

    .
    ├── formidable_color_picker
    │   ├── apps.py
    │   ├── __init__.py
    │   ├── serializers.py
    ├── setup.cfg
    └── setup.py

Loading the field for building time
===================================

The first file we're going to browse is :file:`serializers.py`. Here's a minimal version of it:


.. code-block:: python

    from formidable.register import load_serializer, FieldSerializerRegister
    from formidable.serializers.fields import FieldSerializer, BASE_FIELDS

    field_register = FieldSerializerRegister.get_instance()


    @load_serializer(field_register)
    class ColorPickerFieldSerializer(FieldSerializer):

        type_id = 'color_picker'

        class Meta(FieldSerializer.Meta):
            fields = BASE_FIELDS

Then you're going to need to make sure that Django would catch this file at startup, and thus load the Serializer. It's done via the :file:`apps.py` file.

.. code-block:: python

    from __future__ import absolute_import
    from django.apps import AppConfig


    class FormidableColorPickerConfig(AppConfig):
        """
        Formidable Color Picker configuration class.
        """
        name = 'formidable_color_picker'

        def ready(self):
            """
            Load external serializer when ready
            """
            from . import serializers  # noqa

As you'd do for any other Django application, you can now add this line to your :file:`__init__.py` file at the root of the python module:

.. code-block:: python

    default_app_config = 'formidable_color_picker.apps.FormidableColorPickerConfig'

Check that it's working
-----------------------

Loading the Django shell:

.. code-block:: pycon

    >>> from formidable.serializers import FormidableSerializer
    >>> data = {
        "label": "Color picker test",
        "description": "May I help you pick your favorite color?",
        "fields": [{
            "slug": "color",
            "label": "What is your favorite color?",
            "type_id": "color_picker",
            "accesses": [],
        }]
    }
    >>> instance = FormidableSerializer(data=data)
    >>> instance.is_valid()
    True
    >>> formidable_instance = instance.save()

This means that you can create a form with a field whose type is not in ``django-formidable`` code, but in your module's.

Then you can also retrieve this instance JSON defintion

.. code-block:: pycon

    >>> import json
    >>> print(json.dumps(formidable_instance.to_json(), indent=2))
    {
      "label": "Color picker test",
      "description": "May I help you pick your favorite color?",
      "fields": [
        {
          "slug": "color",
          "label": "What is your favorite color?",
          "type_id": "color_picker",
          "placeholder": null,
          "description": null,
          "accesses": [],
          "validations": [],
          "defaults": [],
        }
      ],
      "id": 42,
      "conditions": [],
      "version": 5
    }

Making your field a bit more clever
===================================

Let's say that colors can be expressed in two ways: RGB tuple (``rgb``) or Hexadecimal expression (``hex``). This means your field has to be parametrized in order to store this information at the builder step. Let's imagine your JSON payload would look like:

.. code-block:: json

    {
        "label": "Color picker test",
        "description": "May I help you pick your favorite color?",
        "fields": [{
            "slug": "color",
            "label": "What is your favorite color?",
            "type_id": "color_picker",
            "accesses": [],
            "color_format": "hex"
        }]
    }

You want then to make sure that your user would not send a wrong parameter, as in these BAD examples:

.. code-block:: json

    "color_format": ""
    "color_format": "foo"
    "color_format": "wrong"

For this specific field, you only want one parameter and its key is ``format`` and its values are only ``hex`` or ``rgb``

Let's add some validation in your Serializer, then.

.. code-block:: python

    from formidable.register import load_serializer, FieldSerializerRegister
    from formidable.serializers.fields import FieldSerializer, BASE_FIELDS

    field_register = FieldSerializerRegister.get_instance()

    @load_serializer(field_register)
    class ColorPickerFieldSerializer(FieldSerializer):

        type_id = 'color_picker'

        allowed_formats = ('rgb', 'hex')
        default_error_messages = {
            "missing_parameter": "You need a `format` parameter for this field",
            "invalid_format": "Invalid format: `{format}` is not one of {formats}."
        }

        class Meta(FieldSerializer.Meta):
            config_fields = ('color_format', )
            fields = BASE_FIELDS + ('parameters',)

        def to_internal_value(self, data):
            # A call to this super() will build the parameters dict.
            data = super(ColorPickerFieldSerializer, self).to_internal_value(data)
            # Check if the parameters are compliant
            parameters = data.get('parameters', {})
            if set(parameters.keys()) != {'color_format'}:
                self.fail('missing_parameter')

            format = parameters.get('color_format')
            if format not in self.allowed_formats:
                self.fail("invalid_format",
                          format=format, formats=self.allowed_formats)

            return data

.. note:: Full example

    You may browse this as a complete directly usable example in `the following repository: "django-formidable-color-picker" <https://github.com/peopledoc/django-formidable-color-picker>`_
