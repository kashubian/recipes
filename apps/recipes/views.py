from django.shortcuts import render
from django.views import generic

from .models import Recipe
from .forms import RecipeForm


class RecipesView(generic.ListView):

    model = Recipe


class RecipeView(generic.DetailView):

    model = Recipe
    

class AddRecipeView(generic.edit.CreateView):

    form_class = RecipeForm
    success_url = '/recipes'
    template_name = 'recipes/add_recipe.html'


class UpdateRecipeView(generic.edit.UpdateView):

    model = Recipe
    fields = [
        'title',
        'description'
    ]
    success_url = '/recipes'
    template_name = 'recipes/update_recipe.html'


class DeleteRecipeView(generic.edit.DeleteView):

    model = Recipe
    success_url = '/recipes'
    template_name = 'recipes/delete_recipe.html'
