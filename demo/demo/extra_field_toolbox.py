import re

from django import forms

from formidable.forms.field_builder import FieldBuilder
from formidable.serializers.fields import FieldSerializer, BASE_FIELDS
from formidable.forms.fields import ParametrizedFieldMixin, CharField
from formidable.forms.widgets import TextInput


COLOR_RE = re.compile('^#(?:[0-9a-fA-F]{3}){1,2}$')


class ColorPickerFieldSerializer(FieldSerializer):
    """
    Color picker field serializer, only to be used in tests
    """
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
        data = super(ColorPickerFieldSerializer, self).to_internal_value(data)
        # Check if the parameters are compliant
        format = data.get('color_format')
        if format is None:
            self.fail('missing_parameter')

        if format not in self.allowed_formats:
            self.fail("invalid_format",
                      format=format, formats=self.allowed_formats)
        return data


class ColorPickerWidget(TextInput):
    type_id = 'color_picker'


class ColorPickerField(ParametrizedFieldMixin, CharField):
    """
    Custom Django for fields, to handle validation of color picks.
    """
    widget = ColorPickerWidget

    def to_python(self, value):
        return value

    def validate(self, value):
        super(ColorPickerField, self).validate(value)
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
