import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.db.models import FileField
from .utils import PROTECTED_FILES

# Helper function to delete files associated with a model instance


def delete_model_files(instance):
    # Loop through all fields in the model
    for field in instance._meta.fields:
        # Check if the field is a FileField or ImageField
        if isinstance(field, FileField):
            file_field = getattr(instance, field.name)
            print("-----instance----", instance.__dict__, flush=True)
            print("-----field name-----", field.name, flush=True)
            print("----file_field-----", file_field, flush=True)
            # Get the default file name (if defined) from the field's default attribute
            default_file = field.default if field.default != '' else None
            print("-----default---file----", default_file, flush=True)

            # Ensure the file exists and is not the default file before deleting
            if file_field and file_field.name and file_field.name != default_file and file_field.name not in PROTECTED_FILES:
                # For both local and S3 storage, check using file_field.name
                if file_field.storage.exists(file_field.name):
                    print("-----field name to delete-----",
                          field.name, flush=True)
                    file_field.delete(save=False)
# Generic signal handler for any model with file fields


@receiver(post_delete)
def delete_files_on_model_delete(sender, instance, **kwargs):
    # Call the helper function to delete files for the instance
    delete_model_files(instance)
