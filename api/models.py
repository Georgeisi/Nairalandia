from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Create your models here.
class Posts(models.Model):
    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Post')
    title = models.CharField(max_length=200)
    story = models.TextField(max_length=1000)
    tags = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    is_trending= models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering= ['-created_at']

class Image(models.Model):
    post = models.ForeignKey(Posts, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField()  # Store the public URL of the uploaded image from Cloudinary

    def __str__(self):
        return f"Image for {self.blog_post.title}"

    





# class Image(models.Model):
#     blog_post = models.ForeignKey(Posts, related_name='images', on_delete=models.CASCADE)
#     image_url = models.URLField()  

#     def __str__(self):
#         return f"Image for {self.blog_post.title}"
