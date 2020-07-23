from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('add/', add_image, name='add_image'),
    path('<int:pk>/', image_details, name='image_details')
]
