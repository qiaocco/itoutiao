from django.http import HttpResponse
from rest_framework import mixins, viewsets

from .models import Post
from .serializers import PostSerializer


def index(request):
    return HttpResponse("hello world")


class PostViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
