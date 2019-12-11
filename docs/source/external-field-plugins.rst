===============================
External Field Plugin Mechanism
===============================

.. versionadded:: 3.0.0

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
    |   |── field_builder.py
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
-----------------------------------

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

.. code-block:: json-object

    "color_format": ""
    "color_format": "foo"
    "color_format": "wrong"

For this specific field, you only want one parameter and its key is ``format`` and its values are only ``hex`` or ``rgb``

Let's add some validation in your Serializer, then.

.. code-block:: python

    from rest_framework import serializers
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
            data = super().to_internal_value(data)
            # Check if the parameters are compliant
            format = data.get('color_format')
            if format is None:
                self.fail('missing_parameter')

            if format not in self.allowed_formats:
                self.fail("invalid_format",
                          format=format, formats=self.allowed_formats)

            return data


Load your field for the form filler
===================================

In your Django settings, add or update the ``settings.FORMIDABLE_EXTERNAL_FIELD_BUILDERS`` variable, like this:

.. code-block:: python

    FORMIDABLE_EXTERNAL_FIELD_BUILDERS = {
        "color_picker": 'formidable_color_picker.field_builder.ColorPickerFieldBuilder',
    }

Then this namespace should point at your :class:`ColorPickerFieldBuilder` class, which can be written as follows:

.. important::

    The classes you're pointing at in this settings must be subclasses of :class:`formidable.forms.field_builder.FieldBuilder`.

.. code-block:: python

    import re
    from formidable.forms.fields import ParametrizedFieldMixin, CharField
    from formidable.forms.field_builder import FieldBuilder

    COLOR_RE = re.compile('^#(?:[0-9a-fA-F]{3}){1,2}$')

    class ColorPickerWidget(TextInput):
        """
        This widget class enables to use the :meth:`to_formidable()` helper.
        """
        type_id = 'color_picker'

    class ColorPickerField(ParametrizedFieldMixin, CharField):
        """
        The ColorPickerField should inherit from a ``formidable.forms.fields``
        subclass.
        """
        widget = ColorPickerWidget

        def to_python(self, value):
            return value

        def validate(self, value):
            # Depending on the parent class, it might be a good idea to call
            # super() in order to use the parents validation.
            super().validate(value)
            params = getattr(self, '__formidable_field_parameters', {})
            color_format = params.get('color_format')
            if color_format == 'rgb':
                if value not in ('red', 'green', 'blue'):
                    raise forms.ValidationError("Invalid color: {}".format(value))
            elif color_format == 'hex':
                if not COLOR_RE.match(value):
                    raise forms.ValidationError("Invalid color: {}".format(value))
            else:
                raise forms.ValidationError("Invalid color format.")

    class ColorPickerFieldBuilder(FieldBuilder):
        field_class = ColorPickerField


.. important::

    * The field should inherit from a formidable Field class, to enable :meth:`to_formidable()` and :meth:`to_json()` to be used
    * The ``widget`` associated with the Field should have the ``type_id`` property set to the same than the Serializer.


.. note:: Full example

    You may browse this as a complete directly usable example in `the following repository: "django-formidable-color-picker" <https://github.com/peopledoc/django-formidable-color-picker>`_
