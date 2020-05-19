from rest_framework import serializers
from .models import Mosaic, NewMosaic, Album, Image

class MosaicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mosaic
        fields = '__all__'
        read_only_fields = ['mosaic']

class NewMosaicSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewMosaic
        fields = '__all__'
        read_only_fields = ['mosaic']

class FileListSerializer (serializers.Serializer) :
    image = serializers.ListField(
                       child=serializers.FileField( max_length=100000,
                                         allow_empty_file=False,
                                         use_url=False )
                                )
    def create(self, validated_data):
        album=Album.objects.latest('created_at')
        image=validated_data.pop('image')
        for img in image:
            image=Image.objects.create(image=img,album=album,**validated_data)
        return img

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'