from django.http import HttpResponse
from django.shortcuts import render

from .models import Recipe

# Create views.
# Главная страница, Вывод списка рецептов
def index(request):
    recipes = Recipe.objects.all()
    print(recipes)
    return render(request, 'recipe_catalog/index.html', {'recipes': recipes.order_by('title')})

def about(request):
    return render(request, 'recipe_catalog/about.html')

def recipe_detail(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)
    except Recipe.DoesNotExist:
        return handle_error_404(request)
    recipe = Recipe.objects.get(pk=pk)
    context = {
        'recipe_id': recipe.id,
        'title': recipe.title,
        'cooking_time': recipe.cooking_time,
        'image': recipe.image,
        'description': recipe.description,
        'ingredients': recipe.ingredients.order_by('name'),
    }
    return render(request, 'recipe_catalog/recipe.html', context)

def handle_error_404(request):
    return render(request, 'recipe_catalog/404.html', status=404)
