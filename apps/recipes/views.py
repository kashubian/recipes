from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from .models import Recipe, Ingredient
from .forms import RecipeForm


class RecipesView(generic.ListView):

    model = Recipe


class RecipeView(generic.DetailView):

    model = Recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients_list'] = Ingredient.objects.filter(recipe=self.object.pk)        
        return context
        

class AddRecipeView(generic.edit.CreateView):

    form_class = RecipeForm
    success_url = '/'
    template_name = 'recipes/add_recipe.html'
    

class UpdateRecipeView(generic.edit.UpdateView):

    model = Recipe
    fields = [
        'title',
        'description'
    ]
    template_name = 'recipes/update_recipe.html'

    def get_success_url(self):
        return reverse_lazy('recipes:recipe', args=(self.kwargs['pk'],))


class DeleteRecipeView(generic.edit.DeleteView):

    model = Recipe
    success_url = '/'
    template_name = 'recipes/delete_recipe.html'


class AddIngredientView(generic.edit.CreateView):

    
    model = Ingredient
    fields = [
        'name'
    ]
    success_url = '/'
    template_name = 'recipes/add_ingredient.html'

    def dispatch(self, request, *args, **kwargs):
        self.recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.recipe = self.recipe
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipes:recipe', args=(self.kwargs['pk'],))
        