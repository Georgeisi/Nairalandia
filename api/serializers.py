from rest_framework import serializers
from .models import Posts,Image
# from .utils import upload_image_to_cloudinary


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image_url',)

class PostsSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)  # Nested serializer for images

    class Meta:
        model = Posts
        fields = '__all__'
        depth=2
    

    
    # def create(self, validated_data):
    #     images = validated_data.pop('images', [])
    #     post = Posts.objects.create(**validated_data)

    #     for image_data in images:
    #         # Upload each image to Cloudinary and append the URL to the images list
    #         image_url = upload_image_to_cloudinary(image_data)
    #         post.images.append(image_url)

    #     post.save()
    #     return post