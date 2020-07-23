from rest_framework import serializers
from .models import Image
from io import BytesIO
from django.core.files.base import File
import os
import urllib.parse
import urllib.request
import urllib.error
import pathlib
import PIL


class ImageSerializer(serializers.ModelSerializer):
    form_url = serializers.URLField(required=False)
    form_file = serializers.FileField(required=False)
    file = serializers.ImageField(required=False)

    def validate(self, attrs):
        form_url = attrs.get('form_url', None)
        form_file = attrs.get('form_file', None)
        if (not form_url and not form_file) or (form_url and form_file):
            raise serializers.ValidationError("only form_url or only form_file is required")
        elif form_url:
            _, ext = os.path.splitext(form_url)
            allowed_extensions = ['.jpg', '.png', '.bmp']
            if ext not in allowed_extensions:
                raise serializers.ValidationError({"form_url": f"{allowed_extensions}"})
        elif form_file:
            try:
                PIL.Image.open(form_file)
            except PIL.UnidentifiedImageError:
                raise serializers.ValidationError("form_file is not image")
        return attrs

    def create(self, validated_data):
        form_url = validated_data.get('form_url', None)
        form_file = validated_data.get('form_file', None)
        image_instance = Image()
        if form_url:
            file_name = os.path.basename(urllib.parse.urlparse(form_url).path)
            try:
                response = urllib.request.urlopen(form_url)
            except urllib.error.HTTPError as e:
                raise serializers.ValidationError({"form_url": e})
            django_file = File(BytesIO(response.read()))
            image_instance.file.save(file_name, django_file)

        elif form_file:
            image_instance.file = form_file
        image_instance.save()
        return image_instance

    class Meta:
        model = Image
        fields = ['file', 'form_url', 'form_file']
