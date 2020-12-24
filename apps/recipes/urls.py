from django.urls import path
from . import views

app_name = 'recipes'
urlpatterns = [
    path('', views.RecipesView.as_view(), name='recipes'),
    path('<uuid:pk>', views.RecipeView.as_view(), name='recipe'),
    path('add-recipe/', views.AddRecipeView.as_view(), name='add_recipe'),
    path('<uuid:pk>/update', views.UpdateRecipeView.as_view(), name='update_recipe'),
    path('<uuid:pk>/delete', views.DeleteRecipeView.as_view(), name='delete_recipe'),
    path('<uuid:pk>/add-ingredient', views.AddIngredientView.as_view(), name='add_ingredient'),
    path('<uuid:pk>/update-ingredient', views.UpdateIngredientView.as_view(), name='update_ingredient'),
    path('<uuid:pk>/delete-ingredient', views.DeleteIngredientView.as_view(), name='delete_ingredient'),
    path('<uuid:pk>/add-step', views.AddStepView.as_view(), name='add_step'),
    path('<uuid:pk>/update-step', views.UpdateStepView.as_view(), name='update_step'),
    path('<uuid:pk>/delete-step', views.DeleteStepView.as_view(), name='delete_step')
]
