import uuid
import requests
from colorfield.fields import ColorField
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.json import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone

from django.core.validators import URLValidator
from .models_utils import (default_json_data_links,
                           default_json_data_social_media)

# Create your models here.


class School(models.Model):
    name = models.CharField(max_length=100, unique=True)
    domain = models.CharField(
        max_length=100, unique=True, null=True, blank=True)
    uuid = models.CharField(max_length=6, unique=True,
                            editable=False)  # No default here
    address = models.CharField(max_length=255)
    primary_color = ColorField(max_length=10, default='#0000FF')
    secondary_color = ColorField(max_length=10, default='#808080')
    premium = models.BooleanField(default=False)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', default='sample_logo.png')
    info = models.TextField(blank=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True,
                             help_text="Upload a promotional video for the school.")
    video_url = models.URLField(
        blank=True, default="https://youtu.be/szjVXpnabmI", null=True, help_text="Or provide a URL to a promotional video for the school.", validators=[URLValidator()])
    video_thumbnail = models.ImageField(
        upload_to='video_thumbnail/', default='main-thumb.png',  blank=True, null=True)
    top_bar_notifications = JSONField(
        encoder=DjangoJSONEncoder,
        default=dict,  # Change from list to dict
        blank=True,
        help_text=_("Dictionary of notifications for the top bar")
    )

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    upcoming_registration = models.CharField(
        max_length=255, null=True, blank=True)
    upcoming_registration_end_date = models.DateField(null=True, blank=True)

    def clean(self):
        # Ensure that both course_name and course_registration_end_date are either provided together or left blank together
        if bool(self.upcoming_registration) != bool(self.upcoming_registration_end_date):
            raise ValidationError(
                'Both course name and course registration end date must be provided together, or both should be left blank.'
            )

        # Ensure course_registration_end_date is greater than today, if provided
        if self.upcoming_registration_end_date and self.upcoming_registration_end_date <= timezone.now().date():
            raise ValidationError(
                'The course registration end date must be a future date.')

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if this is not an existing instance
            if not self.uuid:
                self.uuid = uuid.uuid4().hex[:6].lower()
            super(School, self).save(*args, **kwargs)

            menu_items = [
                ("Home", "-"),
                ("About Us", "-"),
                ("Testimonials", "-"),
                ("News", "-"),
                ("Events", "-"),
                ("Contact Us", "-"),
            ]

            for name, link in menu_items:
                NavigationMenu.objects.get_or_create(
                    school=self,
                    name=name,
                    link=link
                )

            Banner.objects.create(
                school=self
            )

            # Create default FooterContent for the school
            FooterContent.objects.get_or_create(
                school=self,
                defaults={
                    "about_text": "Powered By Learn0Leap",
                    "links": default_json_data_links(),  # Use the default links structure
                    # Use the default social media structure
                    "social_media": default_json_data_social_media()
                }
            )
        else:

            super(School, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}_{self.domain}_{self.uuid}'


class ContactFormEntry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    uuid = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.name} - {self.email}"


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
    banner_video = models.FileField(upload_to='banner_videos/', blank=True,
                                    null=True, default='course-video.mp4', help_text="Upload a promotional video for the school.")
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
    links = models.JSONField()  # Removed default value
    social_media = models.JSONField()  # Removed default value

    def save(self, *args, **kwargs):
        # If links or social_media are empty, set them to the default values
        if not self.links:
            self.links = default_json_data_links()
        if not self.social_media:
            self.social_media = default_json_data_social_media()

        # Call the original save() method
        super(FooterContent, self).save(*args, **kwargs)
