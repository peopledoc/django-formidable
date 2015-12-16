from django.db.models import QuerySet


class FormidableQuerySet(QuerySet):

    def create(self, **kwargs):

        try:
            fields = kwargs.pop('fields')
        except KeyError:
            fields = []

        instance = super(FormidableQuerySet, self).create(**kwargs)

        for field in fields:
            instance.fields.create(**field)

        return instance
