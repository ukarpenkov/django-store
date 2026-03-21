# django-allauth and SITE_ID require a row in django_site; Django 6 sites
# migrations no longer insert the default site automatically.

from django.db import migrations


def create_default_site(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    Site.objects.get_or_create(
        pk=1,
        defaults={
            "domain": "127.0.0.1:8000",
            "name": "Store",
        },
    )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("users", "0002_user_is_verified_email_emailverification"),
    ]

    operations = [
        migrations.RunPython(create_default_site, noop),
    ]
