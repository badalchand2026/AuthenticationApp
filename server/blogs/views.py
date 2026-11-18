
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied

from .models import Blog
from .serializers import BlogSerializer


class BlogListCreateView(generics.ListCreateAPIView):

    serializer_class = BlogSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Blog.objects.all().order_by('-created_at')

        return Blog.objects.filter(
            status='published'
        ).order_by('-created_at')

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminUser()]

        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsAdminUser()]

        return [IsAuthenticated()]

    def get_object(self):
        blog = super().get_object()

        if not self.request.user.is_staff:
            if blog.status != 'published':
                raise PermissionDenied(
                    "You cannot access this blog."
                )

        return blog
