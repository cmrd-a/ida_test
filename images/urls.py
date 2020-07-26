from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

from .views import index, add_image, image_details, ImageViewSet

router = routers.DefaultRouter()
router.register(r'images', ImageViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('add/', add_image, name='add_image'),
    path('<int:pk>/', image_details, name='image_details'),
    url(r'^api/', include(router.urls)),
]
