# -*- coding: utf-8 -*-

from django.views.generic.edit import FormView

from formidable.models import Formidable
import formidable.views
from formidable.views import ContextFormDetail


class FormPreview(FormView):

    model = Formidable
    template_name = 'preview.html'

    def get_form_class(self):
        role = self.request.GET.get('access_id')
        formidable = self.model.objects.get(pk=self.kwargs['pk'])
        return formidable.get_django_form_class(role)

    def form_valid(self, form):
        return self.form_invalid(form)


class DemoContextFormDetail(ContextFormDetail):

    def get_context(self, request, **kwargs):
        return kwargs['role']


class DemoValidateViewFromSchema(formidable.views.ValidateViewFromSchema):

    settings_permission_key = 'FORMIDABLE_PERMISSION_USING'

    def get_formidable_object(self, kwargs):
        formidable = Formidable.objects.get(pk=kwargs['pk'])
        return formidable.to_json()
