from django.core.exceptions import ValidationError
from django.db import models

from jsonfield.fields import JSONField

from formidable import constants
from formidable.register import FieldSerializerRegister


def get_serializer(definition_schema, context=None):
    """
    Return a FormidableSerializer instance, including eventual context.
    """
    from formidable.serializers import FormidableSerializer
    serializer = FormidableSerializer(data=definition_schema)
    # pass context to serializer so we can use it during data validation
    serializer.context.update(context or {})  # If None, will default to {}
    return serializer


class Formidable(models.Model):

    label = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    conditions = JSONField(null=False, blank=False, default=list)

    class Meta:
        app_label = 'formidable'

    def get_django_form_class(self, role=None, field_factory=None):
        """
        Return the django form class associated with the formidable definition.
        If no role_id is provided all the fields are fetched with an
        ``EDITABLE`` access-right.
        :params role: Fetch defined access for the specified role.
        :params field_factory: Instance of Custom field factory if needed.
        :params field_map: Custom Field Builder used by the field_factory.
        """
        from formidable.forms import get_dynamic_form_class
        return get_dynamic_form_class(self, role, field_factory)

    def get_next_field_order(self):
        """
        Get the next order to set on the field to arrive.
        Try to avoid using this method for performance reasons.
        """
        agg = self.fields.aggregate(models.Max('order'))
        return agg['order__max'] + 1 if agg['order__max'] is not None else 0

    @staticmethod
    def from_json(definition_schema, **kwargs):
        """
        Proxy static method to create an instance of ``Formidable`` more
        easily with a given ``definition_schema``.

        :params definition_schema: Schema in JSON/dict

        >>> Formidable.from_json(definition_schema)
        <Formidable: Formidable object>

        """
        context = kwargs.pop("context", {})
        serializer = get_serializer(definition_schema, context)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        return serializer.save(**kwargs)

    def to_json(self):
        from formidable.serializers import FormidableSerializer
        json_data = FormidableSerializer(self).data
        return json_data

    def __str__(self):
        return '{formidable.label}'.format(formidable=self)


class Field(models.Model):

    class Meta:
        unique_together = (('slug', 'form'))
        app_label = 'formidable'

    slug = models.CharField(max_length=256)
    label = models.CharField(max_length=256)
    form = models.ForeignKey(
        Formidable, related_name='fields', on_delete=models.CASCADE
    )
    type_id = models.CharField(
        max_length=256,
        choices=FieldSerializerRegister.get_instance().to_choices()
    )
    placeholder = models.CharField(max_length=256, null=True, blank=True)
    help_text = models.TextField(null=True, blank=True)
    multiple = models.BooleanField(default=False)
    order = models.IntegerField()
    parameters = JSONField(null=True, blank=True, default={})

    def get_next_order(self):
        """
        Get the next order to set on the item to arrive.
        Try to avoid using this method for performance reasons.
        """
        agg = self.items.aggregate(models.Max('order'))
        return agg['order__max'] + 1 if agg['order__max'] is not None else 0

    def __str__(self):
        return '{field.label}'.format(field=self)


class Default(models.Model):

    value = models.CharField(max_length=256, blank=True)
    field = models.ForeignKey(
        Field, related_name='defaults', on_delete=models.CASCADE
    )

    class Meta:
        app_label = 'formidable'

    def __str__(self):
        return '{default.value}'.format(default=self)


class Item(models.Model):
    field = models.ForeignKey(
        Field, related_name='items', on_delete=models.CASCADE
    )
    value = models.TextField()
    label = models.TextField()
    order = models.IntegerField()
    help_text = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'formidable'

    def __str__(self):
        return '{item.label}: {item.value}'.format(item=self)


class Access(models.Model):

    class Meta:
        unique_together = (('field', 'access_id'),)
        app_label = 'formidable'

    field = models.ForeignKey(
        Field, related_name='accesses', on_delete=models.CASCADE
    )
    access_id = models.CharField(max_length=128)
    level = models.CharField(max_length=128, choices=(
        (constants.REQUIRED, 'Required'), (constants.EDITABLE, 'Editable'),
        (constants.HIDDEN, 'Hidden'), (constants.READONLY, 'Readonly'),
    ))

    def __str__(self):
        return '{access.access_id}: {access.level}'.format(
            access=self)


class Validation(models.Model):
    field = models.ForeignKey(
        Field, related_name='validations', on_delete=models.CASCADE
    )
    value = models.CharField(max_length=256)
    type = models.CharField(max_length=256)
    message = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'formidable'

    def __str__(self):
        return '{validation.value}: {validation.type}'.format(
            validation=self)
