# urls.py

from django.urls import path

from . import views

urlpatterns = [
    # The main page that loads the multi-step form
    # path('', views.index_view, name='index'),

    # AJAX endpoints for form actions
    path('load-form/<str:form_name>/', views.load_form_view, name='load_form'),
    path('submit-form/<str:form_name>/',
         views.submit_form_view, name='submit_form'),

    # Optional: AJAX endpoint for live preview updates
    # Make sure you have a corresponding view to handle this
    path('update-preview/<int:school_id>',
         views.update_preview_view, name='update_preview'),
    path('create_school/', views.create_school_with_defaults, name='create_school'),

]
