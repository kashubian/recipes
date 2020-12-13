from django.urls import path
from . import views

app_name = 'recipes'
urlpatterns = [
    path('recipes/', views.RecipesView.as_view(), name='recipes'),
    path('recipes/<slug:slug>', views.RecipeView.as_view(), name='recipe'),
    path('recipes/add-recipe/', views.AddRecipeView.as_view(), name='add_recipe'),
    path('recipes/<slug:slug>/update', views.UpdateRecipeView.as_view(), name='update_recipe'),
    path('recipes/<slug:slug>/delete', views.DeleteRecipeView.as_view(), name='delete_recipe')
]
