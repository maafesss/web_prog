from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    # Простая форма обратной связи с хранением в БД.
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Сообщение от {self.name}"

class Car(models.Model):
    # Каталог машин, для которых можно ставить лайки.
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    # Лайки от пользователей через ManyToMany.
    likes = models.ManyToManyField(User, related_name='liked_cars', blank=True)

    def user_has_liked(self, user):
        # Проверка, ставил ли конкретный пользователь лайк.
        if not user.is_authenticated:
            return False
        return self.likes.filter(id=user.id).exists()

    @property
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return self.name