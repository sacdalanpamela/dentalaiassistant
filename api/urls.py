from django.urls import path

from .views import ask, agent

urlpatterns = [
    path("ask/", ask),
    path("agent/", agent),
]