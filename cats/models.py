from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

User = get_user_model()

class CHOICES(models.TextChoices):
    GRAY = 'Gray', 'Серый'
    BLACK = 'Black', 'Чёрный'
    WHITE = 'White', 'Белый'
    GINGER = 'Ginger', 'Рыжий'
    MIXED = 'Mixed', 'Смешанный'

class Achievement(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Cat(models.Model):
    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16, choices=CHOICES.choices)
    birth_year = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cats')
    achievements = models.ManyToManyField(Achievement, through='AchievementCat', related_name='cats')
    image = models.ImageField(upload_to='cats/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'owner'], name='unique_name_owner')
        ]

    def __str__(self):
        return self.name

    @property
    def age(self):
        return datetime.now().year - self.birth_year

class AchievementCat(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.achievement.name} - {self.cat.name}'