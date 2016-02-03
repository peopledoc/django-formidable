# -*- coding: utf-8 -*-

from django.test import TestCase

from formidable.forms import FormidableForm, fields


class TestForm(FormidableForm):

    title = fields.TitleField(label=u'Onboarding Form')
    helptext = fields.HelpTextField(text='Enter your **address**')
    address = fields.CharField()


class RenderingFormatField(TestCase):

    def setUp(self):
        self.form = TestForm.to_formidable(label='with-format-field')
        self.form_class = self.form.get_django_form_class()

    def test_render_help_text(self):
        form = self.form_class()
        text = form.as_p()
        self.assertIn('<p>Enter your <strong>address</strong></p>', text)
        self.assertNotIn('<span> Enter your **address**', text)

    def test_render_title(self):
        form = self.form_class()
        text = form.as_p()
        self.assertIn('<h4>Onboarding Form</h4>', text)
