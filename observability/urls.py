from django.urls import path

from observability.views import metrics


urlpatterns = [
    path("metrics/",metrics)
]