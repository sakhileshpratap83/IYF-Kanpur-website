# Generated by Django 3.0.4 on 2020-03-29 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_devotee_detail_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='devotee_detail',
            name='slug',
            field=models.SlugField(default='Hare Krishna'),
            preserve_default=False,
        ),
    ]
