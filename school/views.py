import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.http import Http404, HttpResponse
from django.conf import settings
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from django.utils.timezone import get_current_timezone


from .forms import (AboutForm, BannerForm, FooterForm, NavigationMenuForm,
                    NewsForm, SchoolForm, TestimonialForm, ContactForm)
from .models import (AboutSection, Banner, FooterContent, NavigationMenu,
                     NewsArticle, School, Testimonial, ContactFormEntry)
from .utils import fetch_news_and_events_from_lms

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
    news_events = fetch_news_and_events_from_lms('e16e40')
    # Render the template with the context
    return render(request, 'school_preview_template.html', {
        'school': school,
        'navigation': navigation,
        'banner': banner,
        'about_section': about_section,
        'latest_news_articles': latest_news_articles,
        'testimonials': testimonials,
        'footer_content': footer_content,
        'news_events': news_events
    })


def new_update_preview_view(request, school_id=None):
    # Fetch the school instance by ID or return a 404 error if not found
    if school_id:
        school = get_object_or_404(School, pk=school_id)
    else:
        print("-----tt-t--t-", request.school, flush=True)
        if not request.school:
            raise Http404("School not found")
        school = request.school

    # Fetch related objects from the database, ensuring they are related to the fetched school
    navigation = NavigationMenu.objects.filter(school=school)
    navigation_list = list(NavigationMenu.objects.filter(
        school=school).values_list('name', flat=True))
    banner = Banner.objects.filter(school=school).first()
    about_section = AboutSection.objects.filter(school=school).first()
    testimonials = Testimonial.objects.filter(school=school)
    footer_content = FooterContent.objects.filter(school=school).first()
    news_events = fetch_news_and_events_from_lms(school.uuid)

    # Handle datetime conversion for news events
    for news_event in news_events:
        news_event['updated_date'] = parse_datetime(news_event['updated_date'])
        if news_event['updated_date'] and settings.USE_TZ:
            news_event['updated_date'] = news_event['updated_date'].astimezone(
                get_current_timezone())

    # Determine which sections to show
    show_important_notices = any(
        event['posted_as'] == 'Event' for event in news_events)
    show_about_section = about_section is not None
    show_news_section = any(event['posted_as'] ==
                            'News' for event in news_events)
    # Assume you always want to show contact unless specified otherwise
    show_contact_section = True

    # The context dictionary contains all the variables to be passed to the template
    context = {
        'school': school,
        'navigation': navigation,
        'nav_list': navigation_list,
        'banner': banner,
        'about_section': about_section,
        'testimonials': testimonials,
        'footer_content': footer_content,
        'news_events': news_events,
        'LMS_EXTERNAL_URL': settings.LMS_EXTERNAL_URL,
        'form': ContactForm(),
        'show_important_notices': show_important_notices,
        'show_about_section': show_about_section,
        'show_news_section': show_news_section,
        'show_contact_section': show_contact_section,
    }

    # The render function combines the template with the context and returns an HttpResponse object
    return render(request, 'blocks.html', context)


# def new_update_preview_view(request, school_id):
#     # Fetch the school instance by ID or return a 404 error if not found
#     school = get_object_or_404(School, pk=school_id)

#     # Fetch related objects from the database, ensuring they are related to the fetched school
#     # For lists of objects (navigation, latest_news_articles, testimonials), Django queries return QuerySets
#     navigation = NavigationMenu.objects.filter(school=school)
#     # .first() is used to get a single instance or None
#     banner = Banner.objects.filter(school=school).first()
#     about_section = AboutSection.objects.filter(school=school).first()
#     latest_news_articles = NewsArticle.objects.filter(school=school)
#     testimonials = Testimonial.objects.filter(school=school)
#     footer_content = FooterContent.objects.filter(school=school).first()
#     news_events = fetch_news_and_events_from_lms(school.uuid)

#     for news_event in news_events:
#         # Convert string to datetime object
#         news_event['updated_date'] = parse_datetime(news_event['updated_date'])
#         if news_event['updated_date'] and settings.USE_TZ:
#             # Make it timezone-aware, according to your current timezone settings
#             news_event['updated_date'] = news_event['updated_date'].astimezone(
#                 get_current_timezone())

#     # The context dictionary contains all the variables to be passed to the template
#     context = {
#         'school': school,
#         'navigation': navigation,
#         'banner': banner,
#         'about_section': about_section,
#         'latest_news_articles': latest_news_articles,
#         'testimonials': testimonials,
#         'footer_content': footer_content,
#         'news_events': news_events,
#         'LMS_EXTERNAL_URL': settings.LMS_EXTERNAL_URL,
#         'form': ContactForm()
#     }

#     # The render function combines the template with the context and returns an HttpResponse object
#     return render(request, 'updated_2_preview.html', context)


def contact_submit(request):
    if request.method == 'POST':
        print(request.__dict__)
        print("-----2-2-2--2--2-2--")
        form = ContactForm(request.POST)
        if form.is_valid():
            print("---3-3--3-3-0---3")
            # Retrieve form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            uuid = form.cleaned_data['uuid']

            # Fetch the school_id from School model using uuid
            try:
                school_id = School.objects.get(uuid=uuid).id
            except School.DoesNotExist:
                messages.error(request, 'Invalid school identifier.')
                return redirect(request.META.get('HTTP_REFERER', '/'))

            # Create a new ContactFormEntry instance
            entry = ContactFormEntry(
                name=name, email=email, phone=phone, message=message, uuid=uuid)
            entry.save()
            print("---43---4--4-4--")
            messages.success(
                request, 'Your message has been sent successfully!')
            # Redirect to a success page or handle appropriately
            print("----")
            return redirect('new_update_preview', school_id=school_id)
        else:
            print("--------5--5-5--5--")
            # If the form is not valid, re-render the form with error messages
            messages.error(request, 'Please correct the errors below.')
            return redirect(request.META.get('HTTP_REFERER', '/'))


@csrf_exempt
def receive_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.POST['data'])
        logo_file = request.FILES.get('logo', None)
        # Process the received data and file here
        print("Received data:", data)
        if data:
            school, created = School.objects.update_or_create(
                # Assuming 'id' in the data corresponds to 'uuid' in the School model
                uuid=data['id'],
                defaults={
                    'name': data['name'],
                    'domain': data['domain'],
                    'address': data['address'],
                    'phone_no': data.get('phone_no', ''),
                    'email': data.get('email', ''),
                    # Ensuring it's a list
                    # 'top_bar_notifications': data.get('topbar', '')
                }
            )
            if len(school.top_bar_notifications) == 0 and data.get('topbar'):
                school.top_bar_notifications.append(data.get('topbar'))

        if logo_file:
            print("Received file with name:", logo_file.name)
            school.logo.save(logo_file.name, logo_file, save=True)
            print(f'School Updated or Created: {school}')
        return JsonResponse({"status": "success", "message": "Webhook received"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


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
