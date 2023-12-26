from django.contrib import admin

from .models import (AboutSection, Banner, FooterContent, NavigationMenu,
                     NewsArticle, School, Testimonial)

# Register your models here.


class NavigationMenuInline(admin.TabularInline):
    model = NavigationMenu


class BannerInline(admin.TabularInline):
    model = Banner


class AboutSectionInline(admin.TabularInline):
    model = AboutSection


class NewsArticleInline(admin.TabularInline):
    model = NewsArticle


class TestimonialInline(admin.TabularInline):
    model = Testimonial


class FooterContentInline(admin.TabularInline):
    model = FooterContent

# School admin


class SchoolAdmin(admin.ModelAdmin):
    inlines = [
        NavigationMenuInline,
        BannerInline,
        AboutSectionInline,
        NewsArticleInline,
        TestimonialInline,
        FooterContentInline,
    ]


# Register the School admin
admin.site.register(School, SchoolAdmin)
