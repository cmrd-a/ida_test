import os

import PIL
from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['file', 'pk']
        read_only_fields = ['pk', 'file']


class ImageNewSerializer(serializers.ModelSerializer):
    form_url = serializers.URLField(required=False)
    form_file = serializers.FileField(required=False)

    def validate(self, attrs):
        form_url = attrs.get('form_url', None)
        form_file = attrs.get('form_file', None)

        if (not form_url and not form_file) or (form_url and form_file):
            raise serializers.ValidationError({
                "form_url": "only form_url or only form_file is required",
                "form_file": "only form_url or only form_file is required"
            })
        elif form_url:
            _, ext = os.path.splitext(form_url)
            allowed_extensions = ['.jpg', '.png', '.bmp']
            if ext not in allowed_extensions:
                raise serializers.ValidationError(
                    {"form_url": f"the link should lead to files in the following formats {allowed_extensions}"})
        elif form_file:
            try:
                PIL.Image.open(form_file)
            except PIL.UnidentifiedImageError:
                raise serializers.ValidationError({
                    "form_file": "only images allowed"})
        return attrs

    class Meta:
        model = Image
        fields = ['form_url', 'form_file']


class ImageResizeSerializer(serializers.ModelSerializer):
    width = serializers.IntegerField(required=False)
    height = serializers.IntegerField(required=False)

    def validate(self, attrs):
        width = attrs.get('width', None)
        height = attrs.get('height', None)
        if not width and not height:
            raise serializers.ValidationError({
                "width": "width or height is required",
                "height": "width or height is required"
            })
        return attrs

    class Meta:
        model = Image
        fields = ['width', 'height']
