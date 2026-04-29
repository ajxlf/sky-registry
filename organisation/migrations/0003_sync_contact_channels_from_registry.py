from django.db import migrations


def sync_contact_channels(apps, schema_editor):
    Team = apps.get_model("organisation", "Team")
    Team.objects.all().update(contact_channel="")

    # Values taken from the Team Registry spreadsheet.
    Team.objects.filter(name="Agile Avengers").update(
        contact_channel="peacock-bravo, gst-xtv-commerce, gst-xtv-bravo-frontdoor"
    )


def clear_contact_channels(apps, schema_editor):
    Team = apps.get_model("organisation", "Team")
    Team.objects.all().update(contact_channel="")


class Migration(migrations.Migration):
    dependencies = [
        ("organisation", "0002_team_contact_channel"),
    ]

    operations = [
        migrations.RunPython(sync_contact_channels, clear_contact_channels),
    ]
