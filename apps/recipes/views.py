from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe


class RecipesView(ListView):

    model = Recipe


class RecipeView(DetailView):

    model = Recipe
    