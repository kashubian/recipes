from django.contrib import admin
from . import models

admin.site.register([
    models.Recipe,
    models.Ingredient,
    models.Unit,
    models.Step,
    models.Comment,
    models.Tag
])
