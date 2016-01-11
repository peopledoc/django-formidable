# -*- coding: utf-8 -*-
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from formidable.models import Formidable


class FormidableListView(ListView):

    model = Formidable


class FormidableDetailView(DetailView):

    model = Formidable
