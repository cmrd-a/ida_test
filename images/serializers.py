from rest_framework import serializers
from .models import Image
from io import BytesIO
from django.core.files.base import File
import os
from urllib.parse import urlparse
import urllib.request
import urllib


class ImageSerializer(serializers.ModelSerializer):
    form_url = serializers.URLField(required=False)
    form_file = serializers.FileField(required=False)
    file = serializers.FileField(required=False)

    def validate(self, attrs):
        form_url = attrs.get('form_url', None)
        form_file = attrs.get('form_file', None)
        if not form_url and not form_file:
            raise serializers.ValidationError("form_url or form_file is required")
        return attrs

    def create(self, validated_data):
        form_url = validated_data.get('form_url', None)
        form_file = validated_data.get('form_file', None)
        image_instance = Image()
        if form_url:
            file_name = os.path.basename(urlparse(form_url).path)
            request = urllib.request.urlopen(form_url)
            django_file = File(BytesIO(request.read()))
            image_instance.file.save(file_name, django_file)
        elif form_file:
            image_instance.file = form_file

        image_instance.save()
        return image_instance

    class Meta:
        model = Image
        fields = ['file', 'form_url', 'form_file']
