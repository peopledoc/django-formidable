# -*- coding: utf-8 -*-

from django.views.generic.edit import FormView

from formidable.models import Formidable


class FormPreview(FormView):

    model = Formidable
    template_name = 'preview.html'

    def get_form_class(self):
        role = self.request.GET.get('access_id')
        formidable = self.model.objects.get(pk=self.kwargs['pk'])
        return formidable.get_django_form_class(role)

    def form_valid(self, form):
        return self.form_invalid(form)
