# forms.py

from django import forms

from .models import (AboutSection, Banner, FooterContent, NavigationMenu,
                     NewsArticle, School, Testimonial)


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'domain', 'logo', 'address', 'phone_no', 'email']


class NavigationMenuForm(forms.ModelForm):
    class Meta:
        model = NavigationMenu
        fields = ['name', 'link']


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['image', 'headline', 'subtext', 'cta_text', 'cta_link']


class AboutForm(forms.ModelForm):
    class Meta:
        model = AboutSection
        fields = ['title', 'content', 'image']


class NewsForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['title', 'summary', 'link', 'image']


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['quote', 'author', 'relation']


class FooterForm(forms.ModelForm):
    class Meta:
        model = FooterContent
        fields = ['about_text', 'links', 'social_media']
