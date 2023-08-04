from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Posts
from .serializers import PostsSerializer
from rest_framework import status
from . models import Posts,Image
from rest_framework.pagination import PageNumberPagination
# from rest_framework.views import APIView
import cloudinary.uploader
# Create your views here.

@api_view(['GET'])
def home(request):
    print(request.method)
    return Response({'name': 'Nairaland'})

@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def testing(request):
    if request.method == 'GET':
        return Response({'message': 'Hello, this ia a get request'})
    elif request.method == 'POST':
        return Response({'message': 'Hello, this ia a post request'})

    return Response({'Info': 'Welcome'})

@api_view(['GET'])
def all_posts(request):
    if request.method=='GET':
        story = Posts.objects.all()
        paginator =PageNumberPagination()
        paginator.page_size=5
        paginated_blogs = paginator.paginate_queryset(story, request)
        serializer = PostsSerializer(paginated_blogs, many=True)
        return paginator.get_paginated_response(serializer.data)
    


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_post(request):
    if request.method == 'POST':
        author= request.user
        serializer =PostsSerializer(data=request.data)
        if serializer.is_valid():
            blog_post = serializer.save(creator=author)
            images_data = request.data.getlist('images')
            for image_data in images_data:
                http_request = request._request
                cloudinary_response = cloudinary.uploader.upload(image_data, request=http_request)
                image_url = cloudinary_response['secure_url']
                Image.objects.create(post=blog_post, image_url=image_url)

            return Response({'message': 'Blog post created successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        blog_posts = Posts.objects.all()
        paginator =PageNumberPagination()
        paginator.page_size=5
        paginated_blogs = paginator.paginate_queryset(blog_posts, request)
        serializer = PostsSerializer(paginated_blogs, many=True)
        return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def get_single_post(request, post_id):
    try:
        blog_post = Posts.objects.get(pk=post_id)
    except Posts.DoesNotExist:
        return Response({'message': 'Blog post does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PostsSerializer(blog_post)
    return Response(serializer.data)



@api_view(['PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def edit_post(request, id):
    if request.method == 'PATCH':
        post = Posts.objects.get(id=id)
        serializer = PostsSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()

        new_images = request.data.getlist('images', [])
        existing_images = Image.objects.filter(post=post)

        if not new_images:
            return Response({"message": "Post updated successfully."}, status=status.HTTP_200_OK)
        for image in existing_images:
            if image.image_url not in new_images:
                cloudinary.uploader.destroy(image.image_url)
                image.delete()
        for image_data in new_images:
            try:
                image = Image.objects.get(post=post, image_url=image_data)
            except Image.DoesNotExist:
                result = cloudinary.uploader.upload(image_data)
                Image.objects.create(post=post, image_url=result['secure_url'])

        return Response({"message": "Post updated successfully."}, status=status.HTTP_200_OK)


    elif request.method == 'DELETE':
        post = Posts.objects.get(id=id)
        post.delete()
        return Response({
            'message': 'Post Deleted Successfully', 'status': True}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserPosts(request):
    author = request.user
    getUser = Posts.objects.filter(creator=author)
    serializer = PostsSerializer(getUser, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def trendingView(request):
    if request.method=='GET':
        story= Posts.objects.filter(is_trending=True)
        paginator =PageNumberPagination()
        paginator.page_size=5
        trends = paginator.paginate_queryset(story, request)
        serializer = PostsSerializer(trends, many=True , partial=True)
        return paginator.get_paginated_response(serializer.data)



@api_view(['GET'])
def latestPosts(request):
    if request.method == 'GET':
        post = Posts.objects.all().order_by('-created_at')
        paginator =PageNumberPagination()
        paginator.page_size=5
        latest = paginator.paginate_queryset(post, request)
        serializer = PostsSerializer(latest, many=True)
        return paginator.get_paginated_response(serializer.data)  

@api_view(['GET'])
def Tags(request,tag):
    if request.method =='GET':
        blog_tag= Posts.objects.filter(tags=tag)
        paginator= PageNumberPagination()
        paginator.page_size=5
        tagger= paginator.paginate_queryset(blog_tag,request)
        serializer = PostsSerializer(tagger, many=True)
        return paginator.get_paginated_response(serializer.data)








