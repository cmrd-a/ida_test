from django.shortcuts import render, get_object_or_404
from images.models import Image


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
