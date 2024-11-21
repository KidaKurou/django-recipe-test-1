from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from recipe_catalog.models import Recipe, Ingredient, RecipeIngredient

class RouteTestCase(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()
        
        # Create test data
        self.ingredient = Ingredient.objects.create(
            name='Test Ingredient', 
            weight=100, 
            weight_ready=80, 
            price=10.50
        )
        
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            description='Test Description',
            cooking_time='00:30:00'
        )
        
        # Add ingredient to recipe
        RecipeIngredient.objects.create(
            recipe=self.recipe, 
            ingredient=self.ingredient
        )

    def test_index_route_accessibility(self):
        """Test that the index page is accessible to anonymous users"""
        response = self.client.get(reverse('recipe_catalog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe_catalog/index.html')

    def test_about_route_accessibility(self):
        """Test that the about page is accessible to anonymous users"""
        response = self.client.get(reverse('recipe_catalog:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe_catalog/about.html')

    def test_recipe_detail_route(self):
        """Test that a specific recipe detail page is accessible"""
        response = self.client.get(reverse('recipe_catalog:recipe_detail', kwargs={'pk': self.recipe.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe_catalog/recipe.html')

    def test_nonexistent_recipe_route(self):
        """Test route for non-existent recipe returns 404"""
        non_existent_id = Recipe.objects.count() + 1
        response = self.client.get(reverse('recipe_catalog:recipe_detail', kwargs={'pk': non_existent_id}))
        self.assertEqual(response.status_code, 404)
