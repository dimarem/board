from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Aвтора'
        verbose_name_plural = 'Aвторы'

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'


class Ad(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    preview = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='ads')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ads')
    dt_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])


class Feedback(models.Model):
    content = models.CharField(max_length=500)
    accepted = models.BooleanField(default=False)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='feedbacks')

    def __str__(self):
        return f'{self.content[0:100]}...'
