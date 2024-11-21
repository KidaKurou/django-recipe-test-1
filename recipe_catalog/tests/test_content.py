from django.test import TestCase
from django.urls import reverse
from recipe_catalog.models import Recipe, Ingredient, RecipeIngredient
from datetime import timedelta
from decimal import Decimal

class ContentTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test ingredients
        cls.flour = Ingredient.objects.create(
            name='Flour', 
            weight=1000, 
            weight_ready=900, 
            price=Decimal('2.50')
        )
        
        cls.water = Ingredient.objects.create(
            name='Water', 
            weight=1000, 
            weight_ready=1000, 
            price=Decimal('0.10')
        )
        
        # Create multiple test recipes for sorting
        cls.recipes = [
            Recipe.objects.create(
                title='Cake', 
                description='Sweet cake', 
                cooking_time=timedelta(minutes=60)
            ),
            Recipe.objects.create(
                title='Apple Pie', 
                description='Delicious pie', 
                cooking_time=timedelta(minutes=45)
            ),
            Recipe.objects.create(
                title='Bread', 
                description='Simple bread', 
                cooking_time=timedelta(minutes=30)
            )
        ]
        
        # Link ingredients to recipes
        for recipe in cls.recipes:
            RecipeIngredient.objects.create(recipe=recipe, ingredient=cls.flour)
            RecipeIngredient.objects.create(recipe=recipe, ingredient=cls.water)

    def test_ingredient_creation(self):
        """Test correct ingredient object creation"""
        self.assertEqual(self.flour.name, 'Flour')
        self.assertEqual(self.flour.weight, 1000)
        self.assertEqual(self.flour.weight_ready, 900)
        self.assertEqual(self.flour.price, Decimal('2.50'))

    def test_recipe_creation(self):
        """Test correct recipe object creation"""
        recipe = self.recipes[0]
        self.assertTrue(recipe.ingredients.exists())
        self.assertEqual(recipe.cooking_time, timedelta(minutes=60))

    def test_ingredients_alphabetical_order(self):
        """Test ingredients are sorted alphabetically"""
        recipe = self.recipes[0]
        recipe_ingredients = recipe.ingredients.order_by('name')
        self.assertEqual(list(recipe_ingredients), [self.flour, self.water])

    def test_recipes_alphabetical_order(self):
        """Test recipes are sorted alphabetically on index page"""
        response = self.client.get(reverse('recipe_catalog:index'))
        recipes_in_context = response.context['recipes']
        
        sorted_titles = [recipe.title for recipe in recipes_in_context]
        self.assertEqual(sorted_titles, sorted(sorted_titles))

    def test_recipe_ingredient_relationship(self):
        """Test many-to-many relationship between recipes and ingredients"""
        recipe = self.recipes[0]
        self.assertEqual(recipe.ingredients.count(), 2)
        self.assertIn(self.flour, recipe.ingredients.all())
        self.assertIn(self.water, recipe.ingredients.all())