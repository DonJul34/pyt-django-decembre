from django.urls import path
from . import views

urlpatterns = [
    path('generate_text/', views.generate_poem, name='generate_text'),
]
