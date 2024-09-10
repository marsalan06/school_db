from django.apps import AppConfig


class SchoolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'school'

    def ready(self):
        # Import the generic file deletion signal
        from .signals import delete_files_on_model_delete
        from django.db.models import signals
        from .models import School, Banner, AboutSection, NewsArticle, Testimonial

        # Connect the post_delete signal to models with file fields
        signals.post_delete.connect(
            delete_files_on_model_delete, sender=School)
        signals.post_delete.connect(
            delete_files_on_model_delete, sender=Banner)
        signals.post_delete.connect(
            delete_files_on_model_delete, sender=AboutSection)
        signals.post_delete.connect(
            delete_files_on_model_delete, sender=NewsArticle)
        signals.post_delete.connect(
            delete_files_on_model_delete, sender=Testimonial)
