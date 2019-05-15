from django.db import models
from apps.models import BaseModel


class Post(BaseModel):
    author_id = models.IntegerField()
    title = models.CharField(max_length=128, default='', db_index=True)
    orig_url = models.CharField(max_length=255, default='')
    can_comment = models.BooleanField(default=True)
    content = models.TextField()


class PostTag(BaseModel):
    post_id = models.IntegerField()
    tag_id = models.IntegerField()
