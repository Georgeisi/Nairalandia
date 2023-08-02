from django.urls import path,include
from . import views


# from django.conf import settings
# from django.conf.urls.static import static


urlpatterns = [
    path('', views.home ),
    path('testing/', views.testing),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('posts/', views.all_posts),
    path('create/', views.create_post),
    path('single-post/<int:post_id>/', views.get_single_post),
    path('userposts/', views.getUserPosts),
    path('trending/', views.trendingView),
    path('latest/', views.latestPosts),
    path('edit/<int:id>/', views.edit_post),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)