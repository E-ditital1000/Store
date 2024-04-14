from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
import cloudinary
from cloudinary.uploader import upload

class Command(BaseCommand):
    help = 'Collects static files and uploads them to Cloudinary'

    def handle(self, *args, **options):
        # Collect static files
        call_command('collectstatic', '--no-input')

        # Cloudinary configuration
        cloudinary.config(
        cloud_name='dfueppsdg',
        api_key='616474895267773',
        api_secret='JN2GsI5yw6_rGf8-dzMW-2MjWoo'
    )

        static_root = "C:/Users/ELVIS/Desktop/store/store/static"  # Adjust this path to your STATIC_ROOT
        upload_result = upload(static_root, folder="static", use_filename=True, overwrite=True)

        self.stdout.write(self.style.SUCCESS(f"Uploaded {len(upload_result['uploaded'])} static files to Cloudinary"))
