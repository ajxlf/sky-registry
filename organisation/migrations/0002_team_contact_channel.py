from django.db import migrations, models


def populate_contact_channels(apps, schema_editor):
    Team = apps.get_model("organisation", "Team")
    sample_channels = [
        "#payments-platform",
        "#identity-services",
        "teams://Core API Support",
    ]
    for index, team in enumerate(Team.objects.order_by("id")):
        if not team.contact_channel:
            team.contact_channel = sample_channels[index % len(sample_channels)]
            team.save(update_fields=["contact_channel"])


def clear_contact_channels(apps, schema_editor):
    Team = apps.get_model("organisation", "Team")
    Team.objects.filter(
        contact_channel__in=[
            "#payments-platform",
            "#identity-services",
            "teams://Core API Support",
        ]
    ).update(contact_channel="")


class Migration(migrations.Migration):
    dependencies = [
        ("organisation", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="contact_channel",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.RunPython(populate_contact_channels, clear_contact_channels),
    ]
