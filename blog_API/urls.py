from django.urls import path
from rest_framework import urlpatterns
from . views import PostList, PostDetail, PostListDetailfilter, CreatePost, AdminPostDetail, EditPost, DeletePost
from rest_framework.routers import DefaultRouter

app_name = 'blog_API'
urlpatterns = [
   #path('<str:pk>/', PostDetail.as_view(), name='detailcreate'),
   path('post/', PostDetail.as_view(), name='detailcreate'),
   path('', PostList.as_view(), name='listcreate'),
   path('search/custom/', PostListDetailfilter.as_view(), name='postsearch'),
   #Post Admin
   path('admin/create/', CreatePost.as_view(), name='createpost'),
   path('admin/edit/postdetail/<int:pk>/', AdminPostDetail.as_view(), name='admindetailpost'),
   path('admin/edit/<int:pk>/', EditPost.as_view(), name='editpost'),
   path('admin/delete/<int:pk>/', DeletePost.as_view(), name='deletepost'),
]

# router = DefaultRouter()
# router.register('', PostList, basename='user')
# urlpatterns = router.urls
