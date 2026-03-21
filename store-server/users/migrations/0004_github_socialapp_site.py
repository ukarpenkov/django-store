# allauth фильтрует SocialApp по текущему сайту (SITE_ID). Без M2M «sites»
# запись из админки не находится и /accounts/github/login/ падает с DoesNotExist.

from django.db import migrations


def attach_github_apps_to_site_1(apps, schema_editor):
    SocialApp = apps.get_model("socialaccount", "SocialApp")
    Site = apps.get_model("sites", "Site")
    site = Site.objects.filter(pk=1).first()
    if not site:
        return
    for app in SocialApp.objects.filter(provider__iexact="github"):
        if not app.sites.filter(pk=site.pk).exists():
            app.sites.add(site)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("socialaccount", "0006_alter_socialaccount_extra_data"),
        ("users", "0003_default_site_for_allauth"),
    ]

    operations = [
        migrations.RunPython(attach_github_apps_to_site_1, noop),
    ]
