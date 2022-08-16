from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    """Модель Group."""
    title = models.CharField("group title", max_length=200)
    slug = models.SlugField("group slug", unique=True)
    description = models.TextField("group description")

    def __str__(self) -> str:
        """Метод вывода названия группы."""
        return self.title


class Post(models.Model):
    """Модель Post."""
    text = models.TextField("post text")
    pub_date = models.DateTimeField("post publication date", auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
    )
