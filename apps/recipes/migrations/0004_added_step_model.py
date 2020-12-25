# Generated by Django 3.1.4 on 2020-12-21 17:15

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_added_unit_model_renamed_description_to_preparation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='preparation',
        ),
        migrations.AddField(
            model_name='recipe',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('instruction', models.TextField()),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
    ]