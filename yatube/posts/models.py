from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    """Модель Group."""
    title = models.CharField("Название группы", max_length=200)
    slug = models.SlugField("Slug группы", unique=True)
    description = models.TextField("Описание группы")

    def __str__(self) -> str:
        """Метод вывода названия группы."""
        return self.title


class Post(models.Model):
    """Модель Post."""
    text = models.TextField("Текст поста")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Автор",
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name="Группа",
    )
