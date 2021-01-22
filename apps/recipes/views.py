from django.shortcuts import render, reverse, redirect
from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect

from .models import Recipe, Ingredient, Step
from .forms import RecipeForm


class RecipesView(generic.ListView):

    model = Recipe
    context_object_name = 'recipes'


class RecipeView(generic.DetailView):

    model = Recipe
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients_list'] = Ingredient.objects.filter(recipe=self.object.pk)
        context['steps_list'] = Step.objects.filter(recipe=self.object.pk)
        return context
        

class AddRecipeView(LoginRequiredMixin, generic.edit.CreateView):

    form_class = RecipeForm
    success_url = '/'
    template_name = 'recipes/add_recipe.html'

    def form_valid(self, form):
        if self.request.user.is_verified:
            form.instance.owner = self.request.user
            return super(AddRecipeView, self).form_valid(form)
        else:
            return HttpResponseRedirect(reverse('recipes:not_verified_user'))

    def get_success_url(self):
        return reverse_lazy('recipes:recipe', kwargs={'pk' : self.object.pk})


def not_verified_user(request):
    return render(request, "recipes/not_verified_user.html")


def add_to_favorite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe.favorite.filter(id=request.user.id).exists():
        recipe.favorite.remove(request.user)
        return redirect('/')

    else:
        recipe.favorite.add(request.user)
        return redirect('/')
    
    
class UpdateRecipeView(LoginRequiredMixin, generic.edit.UpdateView):

    model = Recipe
    fields = [
        'title',
        'description'
    ]
    template_name = 'recipes/update_recipe.html'

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only owners can update recipe """
        obj = self.get_object()
        if obj.owner != self.request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('recipes:recipe', args=(self.kwargs['pk'],))


class DeleteRecipeView(LoginRequiredMixin, generic.edit.DeleteView):

    model = Recipe
    success_url = '/'
    template_name = 'recipes/delete_recipe.html'

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only owners can update recipe """
        obj = self.get_object()
        if obj.owner != self.request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class AddIngredientView(LoginRequiredMixin, generic.edit.CreateView):

    model = Ingredient
    fields = [
        'name',
        'amount',
        'unit'
    ]
    success_url = '/'
    template_name = 'recipes/add_ingredient.html'

    def dispatch(self, request, *args, **kwargs):
        self.recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])

        if self.recipe.owner != self.request.user:
            return HttpResponseForbidden()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.recipe = self.recipe
        return super().form_valid(form)

    def get_success_url(self):

        if 'add_another' in self.request.POST:
            url = reverse_lazy('recipes:add_ingredient', kwargs={'pk': self.object.recipe_id})

        else:
            url = reverse_lazy('recipes:recipe', kwargs={'pk': self.object.recipe_id})

        return url 


class UpdateIngredientView(LoginRequiredMixin, generic.edit.UpdateView):

    model = Ingredient
    fields = [
        'name',
        'amount',
        'unit'
    ]
    template_name = 'recipes/update_ingredient.html'

    def get_success_url(self):
        return reverse_lazy('recipes:recipe', kwargs={'pk': self.object.recipe_id})


class DeleteIngredientView(LoginRequiredMixin, generic.edit.DeleteView):

    model = Ingredient

    def get_success_url(self):
        return reverse_lazy('recipes:recipe', kwargs={'pk': self.object.recipe_id})


class AddStepView(LoginRequiredMixin, generic.edit.CreateView):

    model = Step
    fields = [
        'instruction'
    ]
    template_name = 'recipes/add_step.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])

        if self.recipe.owner != self.request.user:
            return HttpResponseForbidden()
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.recipe = self.recipe
        return super().form_valid(form)

    def get_success_url(self):

        if 'add_another' in self.request.POST:
            url = reverse_lazy('recipes:add_step', kwargs={'pk': self.object.recipe_id})

        else:
            url = reverse_lazy('recipes:recipe', kwargs={'pk': self.object.recipe_id})

        return url


class UpdateStepView(LoginRequiredMixin, generic.edit.UpdateView):

    model = Step
    fields = [
        'instruction'
    ]
    template_name = 'recipes/update_step.html'

    def get_success_url(self):
        return reverse_lazy('recipes:recipe', kwargs={'pk': self.object.recipe_id})


class DeleteStepView(LoginRequiredMixin, generic.edit.DeleteView):

    model = Step
    
    def get_success_url(self):
        return reverse_lazy('recipes:recipe', kwargs={'pk': self.object.recipe_id})
        