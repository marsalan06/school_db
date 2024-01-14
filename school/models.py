import uuid

from colorfield.fields import ColorField
from django.db import models

from .models_utils import (default_json_data_links,
                           default_json_data_social_media)

# Create your models here.


class School(models.Model):
    name = models.CharField(max_length=100, unique=True)
    domain = models.CharField(max_length=100, unique=True)
    uuid = models.CharField(max_length=5, default=uuid.uuid4().hex[:5].lower())
    address = models.CharField(max_length=255)
    primary_color = ColorField(max_length=10, default='#0000FF')
    secondary_color = ColorField(max_length=10, default='#808080')
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', default='sample_logo.png')

    def __str__(self):
        return f'{self.name}_{self.domain}_{self.uuid}'


class NavigationMenu(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}_{self.school}'


class Banner(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='banners/', default='sample_banner.jpeg')
    headline = models.CharField(
        max_length=200, default="Welcome To ABC School")
    subtext = models.TextField(
        default="A place of excellence in learning and teaching")
    cta_text = models.CharField(max_length=100, null=True, blank=True)
    cta_link = models.CharField(max_length=100, null=True, blank=True)


class AboutSection(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='About Us')
    content = models.TextField(default='Detailed text about the school')
    image = models.ImageField(
        upload_to='about-section/', default='about-section-sample.png')


class NewsArticle(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='PTA Announcement')
    summary = models.TextField(
        default="This Quarter PTA will be held on the 2nd Saturday")
    link = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='news/', default='sample-news.png')


class Testimonial(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    quote = models.TextField(
        default="This school has been a fantastic experience for my child.")
    author = models.CharField(max_length=100, default="Mr Abc Xyz")
    relation = models.CharField(max_length=100, default="Father Of Ijk")


class FooterContent(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    about_text = models.TextField(default="Short text about the school.")
    links = models.JSONField(default=default_json_data_links)
    social_media = models.JSONField(default=default_json_data_social_media)
