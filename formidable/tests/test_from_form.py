
from django.test import TestCase

from formidable.models import Formidable
from formidable.forms import FormidableForm
from formidable.forms import fields


class MyForm(FormidableForm):

    mytext = fields.CharField(label='My Text')


class TestFromDjangoForm(TestCase):

    def test_text_field(self):
        initial_count = Formidable.objects.count()
        form = MyForm.to_formidable(label=u'tutu')
        self.assertEquals(initial_count + 1, Formidable.objects.count())
        self.assertTrue(form.fields.filter(
            slug=u'mytext', type_id=u'text', label='My Text'
        ).exists())
