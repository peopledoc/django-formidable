from django.test import TestCase

from formidable.forms.validations.functions import IsEmpty


class ValidationFunctionTest(TestCase):

    def test_is_empty(self):
        func = IsEmpty()
        self.assertTrue(func(None))
        self.assertTrue(func(''))
        self.assertTrue(func(False))
        self.assertTrue(func(0))
        self.assertTrue(func(""))
        self.assertFalse(func("tutu"))
        self.assertFalse(func(True))
        self.assertFalse(func(1))
