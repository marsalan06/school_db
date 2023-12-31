from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

from .forms import (AboutForm, BannerForm, FooterForm, NavigationMenuForm,
                    NewsForm, SchoolForm, TestimonialForm)
from .models import (AboutSection, Banner, FooterContent, NavigationMenu,
                     NewsArticle, School, Testimonial)

# Create your views here.


# Loads a form based on the provided `form_name` parameter.
def load_form_view(request, form_name):
    form_classes = {
        'school': SchoolForm,
        'navigation': NavigationMenuForm,
        'banner': BannerForm,
        'about': AboutForm,
        'news': NewsForm,
        'testimonial': TestimonialForm,
        'footer': FooterForm,
    }
    form_class = form_classes.get(form_name)
    if form_class:
        form = form_class()
        context = {'form': form, 'form_name': form_name}
        return render(request, f'partials/{form_name}_form.html', context)
    return JsonResponse({'error': 'Invalid form name'}, status=400)


# Handles form submissions and saves the data to the associated model.
def submit_form_view(request, form_name):
    form_classes = {
        'school': SchoolForm,
        'navigation': NavigationMenuForm,
        'banner': BannerForm,
        'about': AboutForm,
        'news': NewsForm,
        'testimonial': TestimonialForm,
        'footer': FooterForm,
    }
    form_class = form_classes.get(form_name)
    if form_class:
        if form_name == 'school':
            form = form_class(request.POST, request.FILES)
            if form.is_valid():
                school = form.save()
                request.session['school_id'] = school.pk
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': form.errors}, status=400)
        else:
            school_id = request.session.get('school_id')
            if not school_id:
                return JsonResponse({'error': 'School object not created yet'}, status=400)
            school = get_object_or_404(School, pk=school_id)
            form = form_class(request.POST, request.FILES)
            if form.is_valid():
                form_instance = form.save(commit=False)
                form_instance.school = school
                form_instance.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Invalid form name'}, status=400)


# Add this view to your urls.py


def index_view(request):
    print("=====testing here===", request.session['school_id'])
    return render(request, 'index.html')


# Generates and returns a live preview of the current school page.


def update_preview_view(request, school_id):
    school = get_object_or_404(School, pk=school_id)

    # Fetch each object. If it does not exist, it will be None
    navigation = NavigationMenu.objects.filter(school=school)
    banner = Banner.objects.filter(school=school).first()
    about_section = AboutSection.objects.filter(school=school).first()
    latest_news_articles = NewsArticle.objects.filter(school=school)
    testimonials = Testimonial.objects.filter(school=school)
    footer_content = FooterContent.objects.filter(school=school).first()

    # Render the template with the context
    return render(request, 'school_preview_template.html', {
        'school': school,
        'navigation': navigation,
        'banner': banner,
        'about_section': about_section,
        'latest_news_articles': latest_news_articles,
        'testimonials': testimonials,
        'footer_content': footer_content
    })


# def check_existing_school_view(request):
#     school_id = request.session.get('school_id')
#     if not school_id:
#         return JsonResponse({'exists': False, 'html': ''})

#     school = get_object_or_404(School, pk=school_id)

#     # Fetch associated objects, if they exist
#     navigation = NavigationMenu.objects
#     banner = Banner.objects.filter(school=school).latest(
#         'created_at') if Banner.objects.filter(school=school).exists() else None
#     about_section = AboutSection.objects.filter(school=school).latest(
#         'created_at') if AboutSection.objects.filter(school=school).exists() else None
#     latest_news_articles = NewsArticle.objects.filter(school=school).order_by(
#         '-created_at')[:5] if NewsArticle.objects.filter(school=school).exists() else None
#     testimonials = Testimonial.objects.filter(school=school).order_by(
#         '-created_at')[:5] if Testimonial.objects.filter(school=school).exists() else None
#     footer_content = FooterContent.objects.filter(school=school).latest(
#         'created_at') if FooterContent.objects.filter(school=school).exists() else None

#     # Render the preview HTML
#     preview_html = render_to_string('school_preview_template.html', {
#         'school': school,
#         'banner': banner,
#         'about_section': about_section,
#         'latest_news_articles': latest_news_articles,
#         'testimonials': testimonials,
#         'footer_content': footer_content
#     })

#     return JsonResponse({'exists': True, 'html': preview_html})
