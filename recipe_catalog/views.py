from django.http import HttpResponse
from django.shortcuts import render

# Create views.
receipt_from_api = [
    {'recipe_id': 1, 'title': 'Блинчики с мясом'},
    {'recipe_id': 2, 'title': 'Котлеты из курицы'},
    {'recipe_id': 3, 'title': 'Борщ'},
    {
        'recipe_id': 4,
        "title": "Лагман",
        "ingredients_list": [
            ('Говядина', 400, 300, 450),
            ('Лапша', 200, 180, 150),
            ('Морковь', 100, 90, 40),
            ('Перец болгарский', 100, 90, 50),
            ('Томат', 100, 80, 30)
        ],
    }
]

# Главная страница, Вывод списка рецептов
def index(request):
    # return HttpResponse("This is the index page.")
    return render(request, 'recipe_catalog/index.html', {'recipes': receipt_from_api})

def about(request):
    return render(request, 'recipe_catalog/about.html')

def recipe_detail(request, pk):
    context = receipt_from_api[pk-1]
    return render(request, 'recipe_catalog/recipe.html', context)
