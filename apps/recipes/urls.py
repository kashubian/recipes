from django.urls import path
from . import views

app_name = 'recipes'
urlpatterns = [
    path('', views.RecipesView.as_view(), name='recipes'),
    path('<uuid:pk>', views.RecipeView.as_view(), name='recipe'),
    path('add-recipe/', views.AddRecipeView.as_view(), name='add_recipe'),
    path('<slug:slug>/update', views.UpdateRecipeView.as_view(), name='update_recipe'),
    path('<slug:slug>/delete', views.DeleteRecipeView.as_view(), name='delete_recipe')
]
