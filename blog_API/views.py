from django.db.models import query
from django.shortcuts import render
from rest_framework import generics, serializers, viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from blog.models import Post
from .serializers import PostSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser,SAFE_METHODS, BasePermission, DjangoModelPermissions, IsAuthenticated
# Create your views here.
class PostUserWritePermission(BasePermission):
    message = "Editing poster is restricted to the author only"
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
        
##--------------------------------------------------------------------
class PostList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    #queryset = Post.objects.all()
    serializer_class = PostSerializer 
    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)

class PostListDetailfilter(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^slug']       # /?search=....
    # '^' starts-with search
    # '=' Exact matches
    # '@' full -text search (sql)
    # '$' regex search
    
##---------------------------------------------------------------------------
class PostDetail(generics.RetrieveAPIView, PostUserWritePermission):
    permission_classes = [PostUserWritePermission]
    queryset = Post.objects.all()
    serializer_class = PostSerializer 

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')

        return get_object_or_404(Post, slug=item)
    
# class PostDetail(generics.ListAPIView):
#     serializer_class = PostSerializer 

#     def get_queryset(self):
#         slug = self.request.query_params.get('slug', None)  
#         return Post.objects.filter(slug=slug)
    

##--------------------------------------------------------------------
# class PostList(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = Post.postObjects.all()
#     def list(self, request):
#         serializer_class = PostSerializer(self.queryset, many=True)
#         return Response(serializer_class.data)

#     def retrieve(self, request, pk=None):
#         post = get_object_or_404(self.queryset, pk=pk)
#         serializer_class = PostSerializer(post)
#         return Response(serializer_class.data)

##----------------------------------------------------------------------------

# class PostList(viewsets.ModelViewSet, PostUserWritePermission):
#     permission_classes = [PostUserWritePermission]
#     serializer_class = PostSerializer

#     def get_object(self, queryset=None, **kwargs):
#         item = self.kwargs.get('pk')
#         return get_object_or_404(Post, slug=item)

#     def get_queryset(self):
#         return Post.objects.all()
    

    


# class PostDetail(viewsets.ModelViewSet, PostUserWritePermission):
#     permission_classes = [PostUserWritePermission]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer 



#Post Admin
# class CreatePost(generics.CreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

class AdminPostDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class EditPost(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class DeletePost(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

##----------------------------------------------------
class CreatePost(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

