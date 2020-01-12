from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class News(models.Model):

    title = models.TextField(verbose_name='Title')
    body = models.TextField(verbose_name='Body')
    view_count = models.IntegerField(verbose_name='View Count', default=0)
    root_category = models.CharField(verbose_name='Root Category', max_length=64)
    category = models.CharField(verbose_name='Category', max_length=64, default='')
    image = models.TextField(verbose_name='Image')
    publish_time = models.TimeField(verbose_name='Publish Time', auto_now=True)
    publish_date = models.DateField(verbose_name='Date', auto_now=True)
    lead = models.TextField(verbose_name='Lead Text')

    class Meta:
        verbose_name_plural = 'NEWS'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.id])


class Category(models.Model):
    name = models.TextField(verbose_name='Root Category', max_length=64)
    user = models.ForeignKey(User, models.CASCADE, )

    def __str__(self):
        return f'{self.name} - {self.user.username}'
