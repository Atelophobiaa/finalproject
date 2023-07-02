from django.urls import path, include
from .views import (
    dna,msg
)

urlpatterns = [
    path('dna', dna.as_view()),
    path('msg', msg.as_view()),
]