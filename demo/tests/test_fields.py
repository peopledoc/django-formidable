# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TestCase

from formidable.forms import BaseDynamicForm, fields


class TestForm(BaseDynamicForm):

    title = fields.TitleField(label='Onboarding Form')
    helptext = fields.HelpTextField(text='Enter your **address**')
    sepa = fields.SeparatorField()


class RenderingFormatField(TestCase):

    def test_render_help_text(self):
        form = TestForm()
        text = form.as_p()
        self.assertIn('<p>Enter your <strong>address</strong></p>', text)
        self.assertNotIn('<span> Enter your **address**', text)
        self.assertNotIn("id_title", text)

    def test_render_title(self):
        form = TestForm()
        text = form.as_p()
        self.assertNotIn("id_helptext", text)
        self.assertIn('<h4>Onboarding Form</h4>', text)

    def test_render_separator(self):
        form = TestForm()
        text = form.as_p()
        self.assertNotIn("id_sepa", text)
        self.assertIn('<hr>', text)
