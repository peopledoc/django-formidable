from rest_framework.generics import RetrieveAPIView

from formidable.models import Formidable
from formidable.serializers import FormidableSerializer


class FormidableDetail(RetrieveAPIView):

    queryset = Formidable.objects.all()
    serializer_class = FormidableSerializer
