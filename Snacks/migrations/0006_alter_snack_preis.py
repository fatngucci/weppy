# Generated by Django 4.1.3 on 2022-12-21 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Snacks', '0005_alter_snack_produkt_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snack',
            name='preis',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
