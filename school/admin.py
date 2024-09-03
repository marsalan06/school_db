from django.contrib import admin
from django.conf import settings
from .models import (AboutSection, Banner, FooterContent, NavigationMenu,
                     NewsArticle, School, Testimonial, ContactFormEntry)

from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .utils import update_lat_lon
# Register your models here.




class NavigationMenuInline(admin.TabularInline):
    model = NavigationMenu
    extra = 1


class BannerInline(admin.TabularInline):
    model = Banner
    extra = 1


class AboutSectionInline(admin.TabularInline):
    model = AboutSection
    extra = 1


class NewsArticleInline(admin.TabularInline):
    model = NewsArticle
    extra = 1


class TestimonialInline(admin.TabularInline):
    model = Testimonial
    extra = 1


class FooterContentInline(admin.TabularInline):
    model = FooterContent
    extra = 1



class SchoolAdmin(admin.ModelAdmin):
    inlines = [
        NavigationMenuInline,
        BannerInline,
        AboutSectionInline,
        NewsArticleInline,
        TestimonialInline,
        FooterContentInline,
    ]
    actions=[update_lat_lon]
  
# Register the School admin
admin.site.register(School, SchoolAdmin)
admin.site.register(ContactFormEntry)
