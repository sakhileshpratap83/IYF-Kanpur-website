# Generated by Django 3.0.4 on 2020-03-29 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_devotee_detail_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devotee_detail',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]