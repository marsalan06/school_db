from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

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


def new_update_preview_view(request, school_id):
    # Fetch the school instance by ID or return a 404 error if not found
    school = get_object_or_404(School, pk=school_id)

    # Fetch related objects from the database, ensuring they are related to the fetched school
    # For lists of objects (navigation, latest_news_articles, testimonials), Django queries return QuerySets
    navigation = NavigationMenu.objects.filter(school=school)
    # .first() is used to get a single instance or None
    banner = Banner.objects.filter(school=school).first()
    about_section = AboutSection.objects.filter(school=school).first()
    latest_news_articles = NewsArticle.objects.filter(school=school)
    testimonials = Testimonial.objects.filter(school=school)
    footer_content = FooterContent.objects.filter(school=school).first()

    # The context dictionary contains all the variables to be passed to the template
    context = {
        'school': school,
        'navigation': navigation,
        'banner': banner,
        'about_section': about_section,
        'latest_news_articles': latest_news_articles,
        'testimonials': testimonials,
        'footer_content': footer_content
    }

    # The render function combines the template with the context and returns an HttpResponse object
    return render(request, 'updated_preview.html', context)


def create_school_with_defaults(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST, request.FILES)
        if form.is_valid():
            school = form.save()

            # Create related objects with default values
            NavigationMenu.objects.create(school=school)
            Banner.objects.create(school=school)
            AboutSection.objects.create(school=school)
            NewsArticle.objects.create(school=school)
            Testimonial.objects.create(school=school)
            FooterContent.objects.create(school=school)

            # Redirect to a success page or another appropriate page
            # replace 'success_page' with your success URL
            return redirect(reverse('update_preview', args=[school.id]))
    else:
        form = SchoolForm()

    return render(request, 'create_school.html', {'form': form})

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
