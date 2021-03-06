# Generated by Django 3.1.4 on 2021-01-22 18:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0006_recipe_owner_is_not_null'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='favorite',
            field=models.ManyToManyField(blank=True, related_name='favorite', to=settings.AUTH_USER_MODEL),
        ),
    ]
