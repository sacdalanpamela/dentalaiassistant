from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from observability.metrics import get_metrics



@api_view(['GET'])
def metrics(request):

    data = get_metrics()

    return Response(data)
