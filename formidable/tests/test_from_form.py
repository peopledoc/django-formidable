# -*- coding: utf-8 -*-
from django.test import TestCase

from formidable.models import Formidable
from formidable.forms import FormidableForm
from formidable.forms import fields


class TestFromDjangoForm(TestCase):

    def test_text_field(self):

        class MyForm(FormidableForm):
            mytext = fields.CharField(label='My Text')

        initial_count = Formidable.objects.count()
        form = MyForm.to_formidable(label=u'tutu')
        self.assertEquals(initial_count + 1, Formidable.objects.count())
        self.assertTrue(form.fields.filter(
            slug=u'mytext', type_id=u'text', label='My Text'
        ).exists())

    def test_dropdown_field(self):
        class MyForm(FormidableForm):
            mydropdown = fields.ChoiceField(label=u'Weapons', choices=(
                ('GUN', 'eagle'), ('SWORD', u'Andúril'))
            )

        initial_count = Formidable.objects.count()
        form = MyForm.to_formidable(label=u'form-with-dropdown')
        self.assertEquals(initial_count + 1, Formidable.objects.count())
        self.assertTrue(form.pk)
        self.assertEquals(form.fields.count(), 1)
        self.assertTrue(form.fields.filter(
            slug=u'mydropdown', type_id=u'dropdown', label='Weapons'
        ).exists())
        field = form.fields.first()
        self.assertEquals(field.items.count(), 2)
        self.assertTrue(
            field.items.filter(key=u'GUN', value=u'eagle').exists()
        )
        self.assertTrue(
            field.items.filter(key=u'SWORD', value=u'Andúril').exists()
        )
