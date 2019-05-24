from django.contrib.auth.models import AbstractUser
from django.db import models

from itoutiao.basemodel import BaseModel


class UserProfile(AbstractUser, BaseModel):
    """
    自定义用户
    """

    intro = models.CharField(max_length=128, default="")
    name = models.CharField(max_length=128, default="", db_index=True)
    nickname = models.CharField(max_length=128, default="")
    email = models.CharField(max_length=191, default="", db_index=True)
    password = models.CharField(max_length=191)
    website = models.CharField(max_length=191, default="")
    github_url = models.CharField(max_length=191, default="")
    last_login_at = models.DateTimeField()
    current_login_at = models.DateTimeField()
    last_login_ip = models.CharField(max_length=100)
    current_login_ip = models.CharField(max_length=100)
    login_count = models.IntegerField()
    active = models.BooleanField()
    icon_color = models.CharField(max_length=7)
    confirmed_at = models.DateTimeField()
    company = models.CharField(max_length=191, default="")
    avatar_id = models.CharField(max_length=20, default="")
    roles = models.ForeignKey("Role", related_name="users", on_delete=models.CASCADE)

    class Meta:
        db_table = "users"
        verbose_name = verbose_name_plural = "用户"

    def __str__(self):
        return self.username


class Role(BaseModel):
    name = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=191)
