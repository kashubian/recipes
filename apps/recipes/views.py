from django.shortcuts import render, reverse, redirect
from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect

from .models import Recipe, Ingredient, Step, Comment
from .forms import RecipeForm, CommentForm


class RecipesView(generic.ListView):

    model = Recipe
    context_object_name = 'recipes'


class FavoriteRecipes(generic.ListView):

    model = Recipe
    template_name = 'recipes/favorite_recipes.html'
    context_object_name = 'favorite_recipes'

    def get_queryset(self):
        favorite_recipes = Recipe.objects.filter(favorite__id=self.request.user.id)
        return favorite_recipes


class AddCommentView(generic.CreateView):

    model = Comment
    
    def dispatch(self, request, *args, **kwargs):
        self.recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        if self.request.user.is_verified:
            form.instance.author = self.request.user
            form.instance.recipe_id = self.recipe.id
            return super(AddCommentView, self).form_valid(form)
        else:
            return HttpResponseRedirect(reverse('recipes:not_verified_user'))
    
    def get_success_url(self):
        return reverse_lazy('recipes:recipe', kwargs={'pk' : self.recipe.id})


class UpdateCommentView(LoginRequiredMixin, generic.edit.UpdateView):

    model = Comment
    form_class = CommentForm
    template_name = 'recipes/update_comment.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if self.request.user != obj.author:
            return HttpResponseForbidden()

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('recipes:recipe', kwargs={'pk': self.object.recipe_id})


class DeleteCommentView(LoginRequiredMixin, generic.edit.DeleteView):

    model = Comment

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if self.request.user != obj.author:
            return HttpResponseForbidden()

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('recipes:recipe', kwargs={'pk': self.object.recipe_id})


class RecipeView(AddCommentView, generic.DetailView):

    model = Recipe
    context_object_name = 'recipe'
    form_class = CommentForm
    template_name = 'recipes/recipe_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        global is_favorite
        is_favorite = False
        if self.object.favorite.filter(id=request.user.id).exists():
            is_favorite = True
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients_list'] = Ingredient.objects.filter(recipe=self.object.pk)
        context['steps_list'] = Step.objects.filter(recipe=self.object.pk)
        context['is_favorite'] = is_favorite
        context['comments_list'] = Comment.objects.filter(recipe=self.object.pk)
        return context
    
    def post(self, request, *args, **kwargs):
        return AddCommentView.post(self, request, *args, **kwargs)



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
    if request.user.is_authenticated:
        recipe = get_object_or_404(Recipe, pk=pk)

        if recipe.favorite.filter(id=request.user.id).exists():
            recipe.favorite.remove(request.user)

        else:
            recipe.favorite.add(request.user)
        
        return redirect(request.META['HTTP_REFERER'])
    
    else:
        return HttpResponseForbidden()

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
        