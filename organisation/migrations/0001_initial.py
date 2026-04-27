import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('leader', models.CharField(max_length=100)),
                ('specialisation', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'departments',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Dependency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flow_description', models.CharField(blank=True, help_text='Short description of what flows between these teams.', max_length=200)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name_plural': 'dependencies',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('manager', models.CharField(max_length=100)),
                ('status', models.CharField(default='Active', max_length=20)),
                ('skills', models.TextField(blank=True, help_text='Comma-separated list of skills, e.g. Python, AWS, Docker')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='organisation.department')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='dependency',
            name='downstream_team',
            field=models.ForeignKey(help_text='The team being depended on (the arrow target).', on_delete=django.db.models.deletion.CASCADE, related_name='upstream_dependencies', to='organisation.team'),
        ),
        migrations.AddField(
            model_name='dependency',
            name='upstream_team',
            field=models.ForeignKey(help_text='The team that depends on another (the arrow source).', on_delete=django.db.models.deletion.CASCADE, related_name='downstream_dependencies', to='organisation.team'),
        ),
    ]
