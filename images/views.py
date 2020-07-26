import os
import urllib
import urllib.error
import urllib.parse
import urllib.request
from io import BytesIO

from PIL import Image as PImage
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from images.models import Image
from .serializers import ImageSerializer, ImageNewSerializer, ImageResizeSerializer


def index(request):
    context = {
        'images': Image.objects.all()
    }
    return render(request, 'index.html', context)


def add_image(request):
    return render(request, 'add_image.html')


def image_details(request, pk):
    context = {
        'image': get_object_or_404(Image, pk=pk)
    }
    return render(request, 'image_details.html', context)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        serializer = ImageNewSerializer(data=request.data)
        if serializer.is_valid():
            form_url = serializer.validated_data.get('form_url', None)
            form_file = serializer.validated_data.get('form_file', None)
            image_instance = Image()
            if form_url:
                file_name = os.path.basename(urllib.parse.urlparse(form_url).path)
                req = urllib.request.Request(form_url)
                try:
                    response = urllib.request.urlopen(req)
                except urllib.error.HTTPError:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={"form_url": "error"})
                django_file = ContentFile(BytesIO(response.read()).getvalue())
                image_instance.file.save(file_name, django_file)

            elif form_file:
                image_instance.file = form_file
            image_instance.save()
            return Response(data=ImageSerializer(image_instance).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ImageResizeSerializer(instance, data=request.data)
        if serializer.is_valid():
            original_image = PImage.open(instance.file.file)
            original_width, original_height = original_image.size
            width = serializer.validated_data.get('width', original_width)
            height = serializer.validated_data.get('height', original_height)
            original_format = original_image.format
            original_image.thumbnail((width, height), PImage.ANTIALIAS)
            file_name = os.path.basename(instance.file.name)
            name, ext = os.path.splitext(file_name)
            image_io = BytesIO()
            original_image.save(image_io, original_format)
            image_content = ContentFile(image_io.getvalue(), f"{name}_thumb.{ext}")
            instance.file.save(f"{name}_resized{ext}", image_content)
            serializer.save()
            return Response(ImageSerializer(instance).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
