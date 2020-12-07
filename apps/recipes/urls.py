from django.urls import path
from .views import RecipesView, RecipeView

app_name = 'recipes'
urlpatterns = [
    path('recipes/', RecipesView.as_view(), name='recipes'),
    path('recipes/<slug:slug>', RecipeView.as_view(), name='recipe')
]
