from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property

from basemodel import BaseModel
from corelib.utils import is_numeric, trunc_utf8


class Post(BaseModel):
    author_id = models.IntegerField()
    title = models.CharField(max_length=128, default="", db_index=True)
    orig_url = models.URLField(max_length=255, default="")
    can_comment = models.BooleanField(default=True)
    content = models.TextField()

    class Meta:
        db_table = "posts"
        verbose_name = verbose_name_plural = "文章"
        ordering = ("-id",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", args=(self.slug,))

    @cached_property
    def abstract_content(self):
        return trunc_utf8(self.content, 100)

    @classmethod
    def get(cls, identifier):
        post = cls.objects.filter(title=identifier).first()
        if post:
            return post
        if is_numeric(identifier):
            return cls.objects.get(pk=identifier)

    @cached_property
    def tags(self):
        tag_ids = PostTag.objects.filter(post_id=self.id).values_list(
            "tag_id", flat=True
        )
        tags = Tag.objects.filter(id__in=(id for id in tag_ids)).values_list(
            "name", flat=True
        )
        return tags

    @classmethod
    def update_or_create(cls, **kwargs):
        tags = kwargs.pop("tags", [])
        obj, created = cls.objects.update_or_create(**kwargs)
        if tags:
            PostTag.update_multi(obj.id, tags)
        return obj, created


class Tag(BaseModel):
    name = models.CharField(max_length=128, default="", db_index=True)

    class Meta:
        db_table = "tags"
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
        db_table = "post_tags"
        verbose_name = verbose_name_plural = "文章-标签"
        ordering = ("-id",)

    def __str__(self):
        return self.post_id, self.tag_id

    @classmethod
    def update_multi(cls, post_id, tags):
        origin_tags = Post.get(post_id).tags
        need_add = set()
        need_del = set()
        for tag in tags:
            if tag not in origin_tags:
                need_add.add(tag)
        for tag in origin_tags:
            if tag not in tags:
                need_del.add(tag)
        need_add_tag_ids = set()
        need_del_tag_ids = set()
        for tag_name in need_add:
            tag = Tag.objects.create(name=tag_name)
            need_add_tag_ids.add(tag.id)
        for tag_name in need_del:
            tag = Tag.objects.get(name=tag_name)
            need_del_tag_ids.add(tag.id)

        if need_del_tag_ids:
            cls.objects.filter(post_id=post_id, tag_id__in=need_del_tag_ids).delete()
        for tag_id in need_add_tag_ids:
            cls.objects.create(post_id=post_id, tag_id=tag_id)
