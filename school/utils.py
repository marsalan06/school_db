import requests
from django.conf import settings
import requests
from geopy.geocoders import Nominatim
from django.contrib import messages
from .models import Testimonial, AboutSection
import random
from faker import Faker

fake = Faker()
def fetch_news_and_events_from_lms(organization_id):
    # Construct the URL. Make sure to replace `lms:8001` with the correct hostname and port as needed.
    url = f'{settings.LMS_SERVER_URL}/api/news-and-events/{organization_id}/'
    print(organization_id)
    try:
        response = requests.get(url)
        # Raises an HTTPError if the response status code is 4XX/5XX
        response.raise_for_status()
        print(response.json())
        return response.json()  # Returns the JSON response
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request sending/receiving process
        print(f"An error occurred: {e}")
        return None

def update_lat_lon(modeladmin, request, queryset):
    geolocator = Nominatim(user_agent="school")

    # Flag to determine if any message needs to be sent
    address_error = False

    for organization in queryset:
        if organization.address:
            print("----org address---", organization.address, flush=True)
            location = geolocator.geocode(organization.address)
            print("-----whats here----", location, flush=True)
            if location:
                organization.latitude = location.latitude
                organization.longitude = location.longitude
                organization.save()
            else:
                address_error = True
        else:
            address_error = True

    if address_error:
        modeladmin.message_user(
            request, "Kindly give correct address", level=messages.ERROR)
    else:
        modeladmin.message_user(
            request, "Latitude and Longitude updated successfully.")

update_lat_lon.short_description = "Update latitude and longitude from address"

# # Define a function to populate 8 Testimonial entities
# def populate_testimonials(modeladmin, request, queryset):
#     for school in queryset:
#         # Populate 8 Testimonial entities
#         for i in range(8):
#             Testimonial.objects.create(
#                 school=school,
#                 quote=f"Testimonial quote {i+1} for {school.name}",
#                 author=f"Author {i+1}",
#                 relation=f"Relation {i+1}"
#             )
#     modeladmin.message_user(request, "Successfully populated 8 Testimonials.")
    
#     from .models import AboutSection

# # Define a function to populate 3 AboutSection entities
# def populate_about_sections(modeladmin, request, queryset):
#     for school in queryset:
#         # Populate 3 AboutSection entities
#         for i in range(3):
#             AboutSection.objects.create(
#                 school=school,
#                 title=f"About Section {i+1} for {school.name}",
#                 content=f"This is detailed information about the school {school.name} for section {i+1}."
#             )
#     modeladmin.message_user(request, "Successfully populated 3 About Sections.")


# Function to create a more structured About Us section text

def generate_about_section_text(school):
    texts = [
        f"{school.name} has been at the forefront of educational excellence for over {fake.random_int(min=10, max=50)} years. "
        f"Our dedicated team of educators and staff strive to provide students with the highest quality education, "
        f"fostering creativity, critical thinking, and a passion for lifelong learning. "
        f"At {school.name}, we believe in creating a nurturing and inclusive environment where every child can thrive and reach their full potential. "
        f"Our programs are designed to meet the unique needs of each student, and we are proud to be a part of their academic journey.",
        
        f"Welcome to {school.name}, where we are committed to delivering an outstanding educational experience. "
        f"With over {fake.random_int(min=10, max=50)} years of tradition, our school continues to lead in academic excellence, innovation, and student support. "
        f"Our mission is to empower students through personalized learning and a supportive community that encourages growth and achievement.",
        
        f"At {school.name}, we take pride in our long-standing tradition of academic excellence, spanning {fake.random_int(min=10, max=50)} years. "
        f"Our experienced faculty members are dedicated to providing a stimulating learning environment that nurtures students' intellectual and personal growth. "
        f"We are committed to preparing our students for success in a rapidly changing world.",
        
        f"{school.name} has been a beacon of educational quality for {fake.random_int(min=10, max=50)} years. "
        f"Our approach focuses on holistic development, ensuring that each student is equipped with the skills and knowledge needed to excel academically and personally. "
        f"Join us in celebrating a legacy of excellence and innovation.",
        
        f"Discover the vibrant educational community at {school.name}. With a rich history of {fake.random_int(min=10, max=50)} years, "
        f"we are dedicated to fostering a supportive and engaging environment where students are encouraged to achieve their best. "
        f"Our programs are crafted to inspire and challenge students, preparing them for future success.",
        
        f"At {school.name}, we are proud of our {fake.random_int(min=10, max=50)} years of excellence in education. "
        f"Our goal is to provide a comprehensive learning experience that promotes academic achievement, personal development, and lifelong learning. "
        f"Experience a school environment where innovation meets tradition.",
        
        f"{school.name} stands out as a leader in educational innovation and quality. For over {fake.random_int(min=10, max=50)} years, we have been dedicated to providing a learning experience that fosters curiosity, creativity, and academic excellence. "
        f"Explore the difference a commitment to education can make.",
        
        f"With {fake.random_int(min=10, max=50)} years of dedication to educational excellence, {school.name} is committed to nurturing each student's potential. "
        f"Our programs are designed to cultivate a love for learning and prepare students for success in a dynamic world. "
        f"Join our community and experience education at its best."
    ]

    return random.choice(texts)

# Populate 8 Testimonial entities using Faker
def populate_testimonials(modeladmin, request, queryset):
    for school in queryset:
        for _ in range(8):  # Loop to create 8 Testimonial entries
            Testimonial.objects.create(
                school=school,
                quote=fake.text(max_nb_chars=200),  # Generate fake quote
                author=fake.name(),  # Generate fake author name
                relation=f"Parent of {fake.first_name()}"  # Generate a relationship
            )
    modeladmin.message_user(request, "Successfully populated 8 Testimonials with fake data.")


# Populate 3 AboutSection entities with enhanced text
def populate_about_sections(modeladmin, request, queryset):
    for school in queryset:
        for i in range(3):  # Loop to create 3 AboutSection entries
            AboutSection.objects.create(
                school=school,
                title=f"About Section {i+1}",
                content=generate_about_section_text(school)  # Generate enhanced content
            )
    modeladmin.message_user(request, "Successfully populated 3 About Sections with detailed content.")