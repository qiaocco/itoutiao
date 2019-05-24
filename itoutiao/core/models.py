from django.db import models
from django.urls import reverse

from itoutiao.corelib.utils import is_numeric
from itoutiao.models import BaseModel


class Post(BaseModel):
    author_id = models.IntegerField()
    title = models.CharField(max_length=128, default="", db_index=True)
    orig_url = models.URLField(max_length=255, default="")
    can_comment = models.BooleanField(default=True)
    content = models.TextField()

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ("-id",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", args=(self.slug,))

    @classmethod
    def get(cls, identifier):
        post = cls.objects.filter(title=identifier).first()
        if post:
            return post
        if is_numeric(identifier):
            return cls.objects.get(identifier).first()

    @property
    def tags(self):
        at_ids = PostTag.objects.filter(PostTag.post_id == self.id).values_list("id")
        tags = Tag.objects.filter(Tag.id__in(id for id in at_ids))


class Tag(BaseModel):
    name = models.CharField(max_length=128, default="", db_index=True)

    class Meta:
        verbose_name = verbose_name_plural = "标签"
        ordering = ("-id",)

    def __str__(self):
        return self.name

    @classmethod
    def get_by_name(cls, name):
        return cls.objects.filter_by(name=name).first()


class PostTag(BaseModel):
    post_id = models.IntegerField()
    tag_id = models.IntegerField()

    class Meta:
        verbose_name = verbose_name_plural = "文章-标签"
        ordering = ("-id",)

    def __str__(self):
        return self.post_id, self.tag_id
