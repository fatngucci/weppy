# Generated by Django 4.1.5 on 2023-01-11 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Snacks', '0010_rename_bewertung_snack_produkt_bewertung_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Snacks.comment')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Subject', related_query_name='Subjects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
