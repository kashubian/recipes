from django import forms
from .models import Recipe, Comment, Tag


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description'
        ]
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content'
        ]
        

class TagForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(Tag.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Tag
        fields = ['tags']