from django.db import models
from apps.core.models import Timestamp
from apps.accounts.models import CustomUser
import uuid
from django.template.defaultfilters import slugify


class Recipe(Timestamp):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    description = models.TextField(blank=True)
    favorite = models.ManyToManyField(CustomUser, related_name='favorite', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)


class Step(Timestamp):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    instruction = models.TextField()

    def __str__(self):
        return self.recipe.title


class Ingredient(Timestamp):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.PositiveSmallIntegerField(blank=True, null=True)
    unit = models.ForeignKey('Unit', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Unit(Timestamp):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    